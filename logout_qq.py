import argparse
import sqlite3
from pathlib import Path


def logout(db_path: Path, qq: str) -> int:
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users "
            "SET cookies=NULL, login_status=2, login_expire_time='1970-01-01T00:00:00Z' "
            "WHERE qq=?",
            (qq,),
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Logout a QQ user from app.db by clearing cookies.")
    parser.add_argument("qq", nargs="?", help="QQ number to logout (e.g. 2110921856)")
    parser.add_argument(
        "--db",
        default=None,
        help="Path to sqlite database (default: auto-detect or ./app.db)",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    default_db = script_dir / "qzone-history" / "qzone-history-main" / "app.db"
    db_path = Path(args.db) if args.db else (default_db if default_db.exists() else script_dir / "app.db")
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    qq = args.qq or input("请输入要退出的QQ号: ").strip()
    if not qq:
        raise SystemExit("QQ号不能为空")

    updated = logout(db_path, qq)
    print(f"updated rows: {updated}")


if __name__ == "__main__":
    main()
