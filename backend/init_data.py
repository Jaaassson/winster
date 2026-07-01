"""初始化数据库数据脚本。"""
import json
from app import create_app
from app.extensions import db
from app.models import Admin, Category, Product, Banner, News, SiteConfig


def init_data():
    """初始化示例数据。"""
    app = create_app()

    with app.app_context():
        db.create_all()

        if Admin.query.filter_by(username="admin").first():
            print("数据已存在，跳过初始化")
            return

        print("开始初始化数据...")

        admin = Admin(
            username="admin",
            nickname="Administrator",
            status=1
        )
        admin.set_password("admin123456")
        db.session.add(admin)

        site_config = SiteConfig(
            id=1,
            site_name=json.dumps({"zh-CN": "Winster外贸", "en-US": "Winster Trading"}, ensure_ascii=False),
            site_title=json.dumps({"zh-CN": "Winster外贸 - 专业的产品供应商", "en-US": "Winster Trading - Professional Product Supplier"}, ensure_ascii=False),
            keywords=json.dumps({"zh-CN": "外贸,产品,批发,采购", "en-US": "trade,products,wholesale,sourcing"}, ensure_ascii=False),
            description=json.dumps({"zh-CN": "专业的外贸供应商，提供优质产品和服务", "en-US": "Professional foreign trade supplier, providing quality products and services"}, ensure_ascii=False),
            company_name="Winster Trading Co., Ltd.",
            phone="+86-xxx-xxxxxxx",
            email="info@winster.com",
            address=json.dumps({"zh-CN": "中国广东省深圳市", "en-US": "Shenzhen, Guangdong, China"}, ensure_ascii=False),
            about_us=json.dumps({"zh-CN": "我们是一家专业的外贸公司，致力于为全球客户提供优质的产品和服务。", "en-US": "We are a professional trading company dedicated to providing quality products and services to customers worldwide."}, ensure_ascii=False),
            facebook="https://facebook.com/winster",
            twitter="https://twitter.com/winster",
            linkedin="https://linkedin.com/company/winster",
            instagram="https://instagram.com/winster"
        )
        db.session.add(site_config)

        cat1 = Category(
            name=json.dumps({"zh-CN": "电子产品", "en-US": "Electronics"}, ensure_ascii=False),
            parent_id=0,
            sort_order=1,
            status=1
        )
        cat2 = Category(
            name=json.dumps({"zh-CN": "家居用品", "en-US": "Home & Garden"}, ensure_ascii=False),
            parent_id=0,
            sort_order=2,
            status=1
        )
        cat3 = Category(
            name=json.dumps({"zh-CN": "服装配饰", "en-US": "Fashion"}, ensure_ascii=False),
            parent_id=0,
            sort_order=3,
            status=1
        )
        db.session.add_all([cat1, cat2, cat3])
        db.session.flush()

        cat4 = Category(
            name=json.dumps({"zh-CN": "智能手机", "en-US": "Smart Phones"}, ensure_ascii=False),
            parent_id=cat1.id,
            sort_order=1,
            status=1
        )
        cat5 = Category(
            name=json.dumps({"zh-CN": "智能手表", "en-US": "Smart Watches"}, ensure_ascii=False),
            parent_id=cat1.id,
            sort_order=2,
            status=1
        )
        cat6 = Category(
            name=json.dumps({"zh-CN": "厨房用品", "en-US": "Kitchen"}, ensure_ascii=False),
            parent_id=cat2.id,
            sort_order=1,
            status=1
        )
        cat7 = Category(
            name=json.dumps({"zh-CN": "床上用品", "en-US": "Bedding"}, ensure_ascii=False),
            parent_id=cat2.id,
            sort_order=2,
            status=1
        )
        db.session.add_all([cat4, cat5, cat6, cat7])
        db.session.flush()

        img1 = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smartphone%20product%20photo%20white%20background&image_size=square"
        img2 = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smart%20watch%20product%20photo%20white%20background&image_size=square"
        img3 = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cookware%20set%20stainless%20steel%20product%20photo&image_size=square"
        img4 = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bedding%20set%20cotton%20product%20photo&image_size=square"

        products = [
            Product(
                category_id=cat4.id,
                name=json.dumps({"zh-CN": "旗舰智能手机 Pro Max", "en-US": "Flagship Smartphone Pro Max"}, ensure_ascii=False),
                description=json.dumps({"zh-CN": "高性能智能手机，配备6.7英寸OLED屏幕，5000万像素摄像头，5000mAh大电池。", "en-US": "High-performance smartphone with 6.7-inch OLED display, 50MP camera, 5000mAh battery."}, ensure_ascii=False),
                images=json.dumps([img1], ensure_ascii=False),
                specs=json.dumps({"屏幕尺寸": "6.7英寸", "处理器": "骁龙8 Gen3", "内存": "12GB", "存储": "256GB", "电池": "5000mAh"}, ensure_ascii=False),
                price_usd=599.99,
                price_cny=4299.00,
                stock=1000,
                moq=10,
                packaging=json.dumps({"zh-CN": "彩盒包装，含充电器、数据线、说明书", "en-US": "Color box package, includes charger, cable, manual"}, ensure_ascii=False),
                sort_order=1,
                is_hot=1,
                status=1
            ),
            Product(
                category_id=cat5.id,
                name=json.dumps({"zh-CN": "智能运动手表", "en-US": "Smart Sports Watch"}, ensure_ascii=False),
                description=json.dumps({"zh-CN": "多功能智能手表，支持心率监测、血氧检测、睡眠跟踪，50米防水。", "en-US": "Multi-functional smart watch with heart rate monitor, blood oxygen, sleep tracking, 50m waterproof."}, ensure_ascii=False),
                images=json.dumps([img2], ensure_ascii=False),
                specs=json.dumps({"屏幕尺寸": "1.4英寸", "续航时间": "14天", "防水等级": "5ATM", "传感器": "心率/血氧/GPS"}, ensure_ascii=False),
                price_usd=129.99,
                price_cny=929.00,
                stock=2000,
                moq=20,
                packaging=json.dumps({"zh-CN": "精美礼盒包装", "en-US": "Gift box packaging"}, ensure_ascii=False),
                sort_order=2,
                is_hot=1,
                status=1
            ),
            Product(
                category_id=cat6.id,
                name=json.dumps({"zh-CN": "不锈钢厨具套装", "en-US": "Stainless Steel Cookware Set"}, ensure_ascii=False),
                description=json.dumps({"zh-CN": "10件套不锈钢厨具套装，含煎锅、汤锅、奶锅等，电磁炉通用。", "en-US": "10-piece stainless steel cookware set with fry pan, soup pot, milk pot, induction compatible."}, ensure_ascii=False),
                images=json.dumps([img3], ensure_ascii=False),
                specs=json.dumps({"材质": "304不锈钢", "件数": "10件", "适用炉灶": "通用", "涂层": "不粘涂层"}, ensure_ascii=False),
                price_usd=89.99,
                price_cny=649.00,
                stock=500,
                moq=5,
                packaging=json.dumps({"zh-CN": "纸箱包装，泡沫保护", "en-US": "Carton box with foam protection"}, ensure_ascii=False),
                sort_order=3,
                is_hot=0,
                status=1
            ),
            Product(
                category_id=cat7.id,
                name=json.dumps({"zh-CN": "纯棉床上四件套", "en-US": "Cotton Bedding Set 4-Piece"}, ensure_ascii=False),
                description=json.dumps({"zh-CN": "100%纯棉床上四件套，亲肤透气，多种花色可选。", "en-US": "100% cotton bedding set, skin-friendly and breathable, multiple patterns available."}, ensure_ascii=False),
                images=json.dumps([img4], ensure_ascii=False),
                specs=json.dumps({"材质": "100%纯棉", "规格": "四件套", "尺寸": "200x230cm", "支数": "40支"}, ensure_ascii=False),
                price_usd=49.99,
                price_cny=359.00,
                stock=800,
                moq=10,
                packaging=json.dumps({"zh-CN": "PVC袋+彩卡", "en-US": "PVC bag + color card"}, ensure_ascii=False),
                sort_order=4,
                is_hot=0,
                status=1
            )
        ]
        db.session.add_all(products)

        banner1 = Banner(
            image_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=banner%20electronics%20promotion%20modern&image_size=landscape_16_9",
            title=json.dumps({"zh-CN": "新品上市，限时优惠", "en-US": "New Arrivals, Limited Time Offer"}, ensure_ascii=False),
            link_url="/products",
            sort_order=1,
            status=1
        )
        banner2 = Banner(
            image_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=banner%20factory%20manufacturing%20industrial&image_size=landscape_16_9",
            title=json.dumps({"zh-CN": "源头工厂，品质保障", "en-US": "Direct Factory, Quality Guaranteed"}, ensure_ascii=False),
            link_url="/about",
            sort_order=2,
            status=1
        )
        banner3 = Banner(
            image_url="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=banner%20global%20shipping%20logistics&image_size=landscape_16_9",
            title=json.dumps({"zh-CN": "全球发货，快速送达", "en-US": "Global Shipping, Fast Delivery"}, ensure_ascii=False),
            link_url="/shipping",
            sort_order=3,
            status=1
        )
        db.session.add_all([banner1, banner2, banner3])

        news1 = News(
            title=json.dumps({"zh-CN": "公司参加2026年春季广交会", "en-US": "Our Company Attends 2026 Spring Canton Fair"}, ensure_ascii=False),
            content=json.dumps({"zh-CN": "我们很高兴地宣布，公司将参加2026年春季广交会，展位号：12.3馆A25。欢迎新老客户莅临参观洽谈。", "en-US": "We are pleased to announce that our company will attend the 2026 Spring Canton Fair. Booth: Hall 12.3, A25. Welcome new and old customers to visit."}, ensure_ascii=False),
            cover_image="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=trade%20show%20exhibition%20booth&image_size=square",
            sort_order=1,
            status=1
        )
        news2 = News(
            title=json.dumps({"zh-CN": "新品发布：智能家居系列", "en-US": "New Product Launch: Smart Home Series"}, ensure_ascii=False),
            content=json.dumps({"zh-CN": "我们推出全新的智能家居产品系列，包括智能灯泡、智能插座、智能开关等，支持语音控制。", "en-US": "We launch a brand new smart home product series, including smart bulbs, smart plugs, smart switches, with voice control support."}, ensure_ascii=False),
            cover_image="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smart%20home%20devices%20collection&image_size=square",
            sort_order=2,
            status=1
        )
        db.session.add_all([news1, news2])

        db.session.commit()
        print("数据初始化完成！")
        print("默认管理员账号：admin / admin123456")


if __name__ == "__main__":
    init_data()
