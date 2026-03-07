from baseline.main import main, run_migrations


class _UpgradeSpy:
    def __init__(self) -> None:
        self.called = False
        self.revision: str | None = None

    def __call__(self, config, revision: str) -> None:
        self.called = True
        self.revision = revision


def test_main(monkeypatch):
    uvicorn_run_called = False

    def fake_run(*args: object, **kwargs: object) -> None:
        nonlocal uvicorn_run_called
        uvicorn_run_called = True

    monkeypatch.setattr("baseline.main.uvicorn_run", fake_run)
    main()
    assert uvicorn_run_called


def test_run_migrations_invokes_alembic(monkeypatch):
    spy = _UpgradeSpy()
    monkeypatch.setattr("baseline.main.command.upgrade", spy)

    run_migrations()

    assert spy.called is True
    assert spy.revision == "head"
