from website import create_app
import threading


def test_background_thread():
    """Checks if background thread that is in
       charge of batch-processing is running
       when the app is.
    """
    app = create_app()

    if app:
        background_thread_present = False

        for thread in threading.enumerate():
            if thread.name == "background":
                background_thread_present = True

        assert (background_thread_present)
    return
