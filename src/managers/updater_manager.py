from typing import Callable, Optional

from managers.timer_manager import TimerManager

class UpdaterManager:
    """
    Manages updates
    """
    exclusive_update = None
    exclusive_callback = None
    is_exclusive_callback = False

    @staticmethod
    def set_exclusive_update(to_update:object, callback: Optional[Callable[[], None]] = None) -> None:
        """
        Sets an exclusive update task.

        Args:
            to_update (object): The task to set as exclusive.
            callback (Optional[Callable[[], None]]): Optional callback to execute after the exclusive update.
        """
        if UpdaterManager.exclusive_update == to_update: return
        UpdaterManager.exclusive_update = to_update
        UpdaterManager.exclusive_callback = callback
        UpdaterManager.is_exclusive_callback = True if callback else False
        
    @staticmethod
    def update() -> None:
        """
        Updates all active timers and update exclusive
        """
        TimerManager.update_timers()
        if UpdaterManager.exclusive_update:
            UpdaterManager.exclusive_update.update()
            if not UpdaterManager.exclusive_update.active and UpdaterManager.is_exclusive_callback:
                UpdaterManager.is_exclusive_callback = False
                UpdaterManager.exclusive_callback()
