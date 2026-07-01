"""迁移 company_name 字段为多语言 JSON 格式。"""
import json
from app import create_app
from app.extensions import db
from app.models import SiteConfig
from app.utils.i18n import get_i18n_field


def migrate():
    app = create_app()
    
    with app.app_context():
        config = SiteConfig.query.filter_by(id=1).first()
        
        if not config:
            print("site_config 记录不存在，跳过迁移")
            return
        
        company_name = config.company_name
        
        if not company_name:
            config.company_name = json.dumps({"zh-CN": "", "en-US": ""}, ensure_ascii=False)
            db.session.commit()
            print("company_name 为空，已设置为默认多语言格式")
            return
        
        try:
            data = json.loads(company_name)
            if isinstance(data, dict):
                print("company_name 已经是 JSON 格式，跳过迁移")
                return
        except (json.JSONDecodeError, TypeError):
            pass
        
        i18n_value = json.dumps(
            {"zh-CN": company_name, "en-US": company_name},
            ensure_ascii=False
        )
        config.company_name = i18n_value
        db.session.commit()
        print(f"company_name 已迁移为多语言格式: {company_name} -> {i18n_value}")
        print("迁移完成！")


if __name__ == "__main__":
    migrate()
