from __future__ import annotations

from typing import Any, Dict, Optional
import os
import sys

try:
    from PySide6.QtCore import QObject, Signal
except Exception:  # pragma: no cover - allow import without Qt in some envs
    class QObject:  # type: ignore
        pass
    class Signal:  # type: ignore
        def __init__(self, *_: Any, **__: Any) -> None:
            pass

# Ensure 'src' is on sys.path for 'hrneowave' imports when executed standalone
_here = os.path.dirname(os.path.abspath(__file__))
_src_root = os.path.normpath(os.path.join(_here, '..', '..'))
if _src_root not in sys.path:
    sys.path.insert(0, _src_root)

try:
    from hrneowave.core.signal_bus import (
        get_signal_bus,
        get_error_bus,
        DataBlock,
        ErrorMessage,
    )
except Exception:
    # Fallback: load the module directly to avoid package __init__ side-effects
    import importlib.util as _il
    from types import ModuleType as _ModuleType

    _signal_path = os.path.join(_src_root, 'hrneowave', 'core', 'signal_bus.py')
    _spec = _il.spec_from_file_location('hrneowave_core_signal_bus', _signal_path)
    if _spec and _spec.loader:
        _mod: _ModuleType = _il.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        get_signal_bus = getattr(_mod, 'get_signal_bus')  # type: ignore[assignment]
        get_error_bus = getattr(_mod, 'get_error_bus')  # type: ignore[assignment]
        DataBlock = getattr(_mod, 'DataBlock')  # type: ignore[assignment]
        ErrorMessage = getattr(_mod, 'ErrorMessage')  # type: ignore[assignment]
    else:
        raise


class UISignalAdapter(QObject):
    """Adaptateur UI ↔ Core pour le SignalBus existant.

    Expose des signaux orientés UI et se connecte aux signaux du core sans
    modifier l'API du core. Fournit des helpers pour envoyer des requêtes UI
    vers le core (p.ex. changement de vue, requêtes d'analyse).
    """

    # Signaux UI de haut niveau
    calibration_data_received = Signal(dict)
    acquisition_data_received = Signal(dict)
    analysis_completed = Signal(dict)
    core_error_occurred = Signal(str)
    session_state_changed = Signal(object)  # SessionState

    def __init__(self) -> None:
        super().__init__()
        self.core_signal_bus = get_signal_bus()
        self.core_error_bus = get_error_bus()
        self.setup_connections()

    def setup_connections(self) -> None:
        """Connecter les signaux du core aux signaux UI.

        Mapping basé sur l'API publiée de `SignalBus` et `ErrorBus`.
        """
        # Acquisition: blocs de données
        try:
            self.core_signal_bus.dataBlockReady.connect(self.on_data_block_ready)  # type: ignore[attr-defined]
        except Exception:
            pass

        # Traitement terminé → résultats d'analyse
        try:
            self.core_signal_bus.processingFinished.connect(self.on_processing_finished)  # type: ignore[attr-defined]
        except Exception:
            pass

        # État de session
        try:
            self.core_signal_bus.sessionStateChanged.connect(self.on_session_state_changed)  # type: ignore[attr-defined]
        except Exception:
            pass

        # Erreurs cœur
        try:
            self.core_error_bus.error_occurred.connect(self.on_core_error)  # type: ignore[attr-defined]
        except Exception:
            pass

    # ---------- Handlers Core → UI ----------
    def on_data_block_ready(self, block: DataBlock) -> None:
        payload = {
            'timestamp': block.timestamp,
            'sample_rate': block.sample_rate,
            'n_channels': block.n_channels,
            'n_samples': block.n_samples,
            'metadata': block.metadata,
        }
        # Délivrer un signal UI générique pour acquisition
        self.acquisition_data_received.emit(payload)

    def on_processing_finished(self, results: Dict[str, Any]) -> None:
        self.analysis_completed.emit(results)

    def on_session_state_changed(self, state: Any) -> None:
        self.session_state_changed.emit(state)

    def on_core_error(self, error: ErrorMessage) -> None:
        try:
            user_message = self._format_error_for_user(error)
        except Exception:
            user_message = "Erreur système inattendue"
        self.core_error_occurred.emit(user_message)

    # ---------- UI → Core helpers ----------
    def request_view_change(self, view_name: str) -> None:
        try:
            self.core_signal_bus.request_view_change(view_name)
        except Exception:
            pass

    def request_analysis(self, params: Dict[str, Any]) -> None:
        try:
            # Utilise le signal prévu pour déclencher une analyse
            self.core_signal_bus.analysisRequested.emit(params)  # type: ignore[attr-defined]
        except Exception:
            pass

    # ---------- Utils ----------
    def _format_error_for_user(self, error: ErrorMessage) -> str:
        level = getattr(error.level, 'value', 'error')
        msg = getattr(error, 'message', 'Erreur inconnue')
        src = getattr(error, 'source', 'core')
        return f"[{level}] {src}: {msg}"


