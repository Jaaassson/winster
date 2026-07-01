-- =====================================================
-- 外贸独立站全栈项目 - 数据库初始化脚本
-- 数据库类型: SQLite 3
-- 创建日期: 2026-06-30
-- =====================================================

-- 启用外键约束
PRAGMA foreign_keys = ON;

-- =====================================================
-- 1. 管理员表 (admin)
-- =====================================================
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_admin_status ON admin(status);
CREATE INDEX IF NOT EXISTS idx_admin_deleted_at ON admin(deleted_at);

-- =====================================================
-- 2. 产品分类表 (category)
-- =====================================================
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER NOT NULL DEFAULT 0,
    sort_order INTEGER NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_category_parent_id ON category(parent_id);
CREATE INDEX IF NOT EXISTS idx_category_sort_order ON category(sort_order);
CREATE INDEX IF NOT EXISTS idx_category_status ON category(status);
CREATE INDEX IF NOT EXISTS idx_category_deleted_at ON category(deleted_at);

-- =====================================================
-- 3. 产品表 (product)
-- =====================================================
CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    images TEXT,
    specs TEXT,
    price_usd DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    price_cny DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    stock INTEGER NOT NULL DEFAULT 0,
    moq INTEGER NOT NULL DEFAULT 1,
    packaging TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_hot TINYINT NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE INDEX IF NOT EXISTS idx_product_category_id ON product(category_id);
CREATE INDEX IF NOT EXISTS idx_product_status ON product(status);
CREATE INDEX IF NOT EXISTS idx_product_is_hot ON product(is_hot);
CREATE INDEX IF NOT EXISTS idx_product_sort_order ON product(sort_order);
CREATE INDEX IF NOT EXISTS idx_product_created_at ON product(created_at);
CREATE INDEX IF NOT EXISTS idx_product_deleted_at ON product(deleted_at);

-- =====================================================
-- 4. 询盘表 (inquiry)
-- =====================================================
CREATE TABLE IF NOT EXISTS inquiry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    quantity INTEGER,
    message TEXT NOT NULL,
    product_id INTEGER,
    is_read TINYINT NOT NULL DEFAULT 0,
    is_replied TINYINT NOT NULL DEFAULT 0,
    replied_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE INDEX IF NOT EXISTS idx_inquiry_email ON inquiry(email);
CREATE INDEX IF NOT EXISTS idx_inquiry_country ON inquiry(country);
CREATE INDEX IF NOT EXISTS idx_inquiry_product_id ON inquiry(product_id);
CREATE INDEX IF NOT EXISTS idx_inquiry_is_read ON inquiry(is_read);
CREATE INDEX IF NOT EXISTS idx_inquiry_is_replied ON inquiry(is_replied);
CREATE INDEX IF NOT EXISTS idx_inquiry_created_at ON inquiry(created_at);
CREATE INDEX IF NOT EXISTS idx_inquiry_deleted_at ON inquiry(deleted_at);

-- =====================================================
-- 5. 新闻资讯表 (news)
-- =====================================================
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    cover_image VARCHAR(255),
    sort_order INTEGER NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_news_status ON news(status);
CREATE INDEX IF NOT EXISTS idx_news_sort_order ON news(sort_order);
CREATE INDEX IF NOT EXISTS idx_news_created_at ON news(created_at);
CREATE INDEX IF NOT EXISTS idx_news_deleted_at ON news(deleted_at);

-- =====================================================
-- 6. 轮播图表 (banner)
-- =====================================================
CREATE TABLE IF NOT EXISTS banner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_url VARCHAR(255) NOT NULL,
    title TEXT,
    button_text VARCHAR(255),
    link_url VARCHAR(255),
    sort_order INTEGER NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_banner_status ON banner(status);
CREATE INDEX IF NOT EXISTS idx_banner_sort_order ON banner(sort_order);
CREATE INDEX IF NOT EXISTS idx_banner_deleted_at ON banner(deleted_at);

-- =====================================================
-- 7. 网站配置表 (site_config)
-- =====================================================
CREATE TABLE IF NOT EXISTS site_config (
    id INTEGER PRIMARY KEY DEFAULT 1,
    site_name TEXT,
    site_title TEXT,
    keywords TEXT,
    description TEXT,
    company_name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(100),
    address TEXT,
    about_us TEXT,
    facebook VARCHAR(255),
    twitter VARCHAR(255),
    linkedin VARCHAR(255),
    instagram VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (id = 1)
);

-- =====================================================
-- 8. 初始化数据
-- =====================================================

-- 初始化默认管理员账号 (密码: admin123456)
-- bcrypt hash for 'admin123456'
INSERT OR IGNORE INTO admin (id, username, password_hash, nickname, status)
VALUES (1, 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYGyJkH/Ks8Xqei', 'Administrator', 1);

-- 初始化网站配置
INSERT OR IGNORE INTO site_config (
    id, site_name, site_title, keywords, description,
    company_name, phone, email, address, about_us,
    facebook, twitter, linkedin, instagram
) VALUES (
    1,
    '{"zh-CN": "Winster外贸", "en-US": "Winster Trading"}',
    '{"zh-CN": "Winster外贸 - 专业的产品供应商", "en-US": "Winster Trading - Professional Product Supplier"}',
    '{"zh-CN": "外贸,产品,批发,采购", "en-US": "trade,products,wholesale,sourcing"}',
    '{"zh-CN": "专业的外贸供应商，提供优质产品和服务", "en-US": "Professional foreign trade supplier, providing quality products and services"}',
    'Winster Trading Co., Ltd.',
    '+86-xxx-xxxxxxx',
    'info@winster.com',
    '{"zh-CN": "中国广东省深圳市", "en-US": "Shenzhen, Guangdong, China"}',
    '{"zh-CN": "我们是一家专业的外贸公司...", "en-US": "We are a professional trading company..."}',
    'https://facebook.com/winster',
    'https://twitter.com/winster',
    'https://linkedin.com/company/winster',
    'https://instagram.com/winster'
);

-- 初始化示例分类
INSERT OR IGNORE INTO category (id, name, parent_id, sort_order, status) VALUES
(1, '{"zh-CN": "电子产品", "en-US": "Electronics"}', 0, 1, 1),
(2, '{"zh-CN": "家居用品", "en-US": "Home & Garden"}', 0, 2, 1),
(3, '{"zh-CN": "服装配饰", "en-US": "Fashion"}', 0, 3, 1),
(4, '{"zh-CN": "智能手机", "en-US": "Smart Phones"}', 1, 1, 1),
(5, '{"zh-CN": "智能手表", "en-US": "Smart Watches"}', 1, 2, 1),
(6, '{"zh-CN": "厨房用品", "en-US": "Kitchen"}', 2, 1, 1),
(7, '{"zh-CN": "床上用品", "en-US": "Bedding"}', 2, 2, 1);

-- 初始化示例产品
INSERT OR IGNORE INTO product (id, category_id, name, description, images, specs, price_usd, price_cny, stock, moq, packaging, sort_order, is_hot, status) VALUES
(1, 4,
 '{"zh-CN": "旗舰智能手机 Pro Max", "en-US": "Flagship Smartphone Pro Max"}',
 '{"zh-CN": "高性能智能手机，配备6.7英寸OLED屏幕，5000万像素摄像头，5000mAh大电池。", "en-US": "High-performance smartphone with 6.7-inch OLED display, 50MP camera, 5000mAh battery."}',
 '["https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smartphone%20product%20photo%20white%20background&image_size=square", "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smartphone%20back%20view%20product%20photo&image_size=square"]',
 '{"屏幕尺寸": "6.7英寸", "处理器": "骁龙8 Gen3", "内存": "12GB", "存储": "256GB", "电池": "5000mAh"}',
 599.99, 4299.00, 1000, 10,
 '{"zh-CN": "彩盒包装，含充电器、数据线、说明书", "en-US": "Color box package, includes charger, cable, manual"}',
 1, 1, 1),
(2, 5,
 '{"zh-CN": "智能运动手表", "en-US": "Smart Sports Watch"}',
 '{"zh-CN": "多功能智能手表，支持心率监测、血氧检测、睡眠跟踪，50米防水。", "en-US": "Multi-functional smart watch with heart rate monitor, blood oxygen, sleep tracking, 50m waterproof."}',
 '["https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smart%20watch%20product%20photo%20white%20background&image_size=square"]',
 '{"屏幕尺寸": "1.4英寸", "续航时间": "14天", "防水等级": "5ATM", "传感器": "心率/血氧/GPS"}',
 129.99, 929.00, 2000, 20,
 '{"zh-CN": "精美礼盒包装", "en-US": "Gift box packaging"}',
 2, 1, 1),
(3, 6,
 '{"zh-CN": "不锈钢厨具套装", "en-US": "Stainless Steel Cookware Set"}',
 '{"zh-CN": "10件套不锈钢厨具套装，含煎锅、汤锅、奶锅等，电磁炉通用。", "en-US": "10-piece stainless steel cookware set with fry pan, soup pot, milk pot, induction compatible."}',
 '["https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cookware%20set%20stainless%20steel%20product%20photo&image_size=square"]',
 '{"材质": "304不锈钢", "件数": "10件", "适用炉灶": "通用", "涂层": "不粘涂层"}',
 89.99, 649.00, 500, 5,
 '{"zh-CN": "纸箱包装，泡沫保护", "en-US": "Carton box with foam protection"}',
 3, 0, 1),
(4, 7,
 '{"zh-CN": "纯棉床上四件套", "en-US": "Cotton Bedding Set 4-Piece"}',
 '{"zh-CN": "100%纯棉床上四件套，亲肤透气，多种花色可选。", "en-US": "100% cotton bedding set, skin-friendly and breathable, multiple patterns available."}',
 '["https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bedding%20set%20cotton%20product%20photo&image_size=square"]',
 '{"材质": "100%纯棉", "规格": "四件套", "尺寸": "200x230cm", "支数": "40支"}',
 49.99, 359.00, 800, 10,
 '{"zh-CN": "PVC袋+彩卡", "en-US": "PVC bag + color card"}',
 4, 0, 1);

-- 初始化示例轮播图
INSERT OR IGNORE INTO banner (id, image_url, title, button_text, link_url, sort_order, status) VALUES
(1, 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=banner%20electronics%20promotion%20modern&image_size=landscape_16_9',
 '{"zh-CN": "新品上市，限时优惠", "en-US": "New Arrivals, Limited Time Offer"}',
 '{"zh-CN": "查看产品", "en-US": "View Products"}',
 '/products', 1, 1),
(2, 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=banner%20factory%20manufacturing%20industrial&image_size=landscape_16_9',
 '{"zh-CN": "源头工厂，品质保障", "en-US": "Direct Factory, Quality Guaranteed"}',
 '{"zh-CN": "了解更多", "en-US": "Learn More"}',
 '/about', 2, 1),
(3, 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=banner%20global%20shipping%20logistics&image_size=landscape_16_9',
 '{"zh-CN": "全球发货，快速送达", "en-US": "Global Shipping, Fast Delivery"}',
 '{"zh-CN": "立即咨询", "en-US": "Inquire Now"}',
 '/inquiry', 3, 1);

-- 初始化示例新闻
INSERT OR IGNORE INTO news (id, title, content, cover_image, sort_order, status) VALUES
(1,
 '{"zh-CN": "公司参加2026年春季广交会", "en-US": "Our Company Attends 2026 Spring Canton Fair"}',
 '{"zh-CN": "我们很高兴地宣布，公司将参加2026年春季广交会，展位号：12.3馆A25。欢迎新老客户莅临参观洽谈。", "en-US": "We are pleased to announce that our company will attend the 2026 Spring Canton Fair. Booth: Hall 12.3, A25. Welcome new and old customers to visit."}',
 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=trade%20show%20exhibition%20booth&image_size=square',
 1, 1),
(2,
 '{"zh-CN": "新品发布：智能家居系列", "en-US": "New Product Launch: Smart Home Series"}',
 '{"zh-CN": "我们推出全新的智能家居产品系列，包括智能灯泡、智能插座、智能开关等，支持语音控制。", "en-US": "We launch a brand new smart home product series, including smart bulbs, smart plugs, smart switches, with voice control support."}',
 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=smart%20home%20devices%20collection&image_size=square',
 2, 1);

-- =====================================================
-- 创建更新时间触发器
-- =====================================================

-- admin 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_admin_updated_at
AFTER UPDATE ON admin
FOR EACH ROW
BEGIN
    UPDATE admin SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- category 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_category_updated_at
AFTER UPDATE ON category
FOR EACH ROW
BEGIN
    UPDATE category SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- product 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_product_updated_at
AFTER UPDATE ON product
FOR EACH ROW
BEGIN
    UPDATE product SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- inquiry 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_inquiry_updated_at
AFTER UPDATE ON inquiry
FOR EACH ROW
BEGIN
    UPDATE inquiry SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- news 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_news_updated_at
AFTER UPDATE ON news
FOR EACH ROW
BEGIN
    UPDATE news SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- banner 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_banner_updated_at
AFTER UPDATE ON banner
FOR EACH ROW
BEGIN
    UPDATE banner SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- site_config 表更新触发器
CREATE TRIGGER IF NOT EXISTS trigger_site_config_updated_at
AFTER UPDATE ON site_config
FOR EACH ROW
BEGIN
    UPDATE site_config SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- =====================================================
-- 完成
-- =====================================================
