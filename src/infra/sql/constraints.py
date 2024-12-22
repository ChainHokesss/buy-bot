from sqlalchemy import UniqueConstraint


def unique_constraint(*columns: str, constraint_name: str | None = None) -> UniqueConstraint:
    return UniqueConstraint(
        *columns,
        name=_constraint_name(
            name=constraint_name if constraint_name else '_'.join(columns), constraint='unique'
        ),
    )


def _constraint_name(*, name: str, constraint: str) -> str:
    post_fix = f'_{constraint}_constraint'
    return f'{name[:63 - len(post_fix)]}{post_fix}'
