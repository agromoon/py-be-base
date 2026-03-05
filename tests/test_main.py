from baseline.main import main, run_migrations


class _UpgradeSpy:
    def __init__(self) -> None:
        self.called = False
        self.revision: str | None = None

    def __call__(self, config, revision: str) -> None:
        self.called = True
        self.revision = revision


def test_main():
    main()
    assert True


def test_run_migrations_invokes_alembic(monkeypatch):
    spy = _UpgradeSpy()
    monkeypatch.setattr("baseline.main.command.upgrade", spy)

    run_migrations()

    assert spy.called is True
    assert spy.revision == "head"
