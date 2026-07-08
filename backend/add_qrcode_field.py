"""为site_config表添加qrcode字段"""
from app import create_app
from app.extensions import db
from sqlalchemy import text

def add_qrcode_field():
    app = create_app()
    with app.app_context():
        try:
            # SQLite不支持IF NOT EXISTS，所以直接执行，如果字段已存在会报错但可忽略
            db.session.execute(text('ALTER TABLE site_config ADD COLUMN qrcode VARCHAR(255)'))
            db.session.commit()
            print("qrcode字段已添加到site_config表")
        except Exception as e:
            db.session.rollback()
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print("qrcode字段已存在，无需添加")
            else:
                print(f"添加字段时出错: {e}")

if __name__ == "__main__":
    add_qrcode_field()