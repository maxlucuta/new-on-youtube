from multiprocessing import Process
from website.utilities.pubsub.subscriber import run_background_task
from website import create_app


def execute_background_tasks(name):
    """Runs subscriber batch processing task for child processes."""

    print(f"Running background process {name}!")
    run_background_task()


def create_processes():
    """ Creates two daemon processes for background batch processing."""

    batch_1 = Process(
        name="batch_1", target=execute_background_tasks, args=("batch_1",))
    batch_2 = Process(
        name="batch_2", target=execute_background_tasks, args=("batch_2",))
    batch_1.daemon = batch_2.daemon = True
    batch_1.start()
    batch_2.start()


if __name__ == "__main__":
    app = create_app()
    create_processes()
    app.run(debug=True)
else:
    gunicorn_app = create_app()
