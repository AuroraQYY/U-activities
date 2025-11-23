-- 植物品种库
CREATE TABLE IF NOT EXISTS plant_species (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '植物通用名',
    scientific_name VARCHAR(100) COMMENT '学名',
    family VARCHAR(50) COMMENT '科属',
    plant_type ENUM('观叶植物', '开花植物', '多肉植物', '果蔬', '草本植物', '乔木', '灌木') DEFAULT '观叶植物',
    difficulty_level ENUM('非常简单', '简单', '中等', '困难', '专家级') DEFAULT '中等',
    light_requirements ENUM('强光', '中光照', '弱光', '耐阴') DEFAULT '中光照',
    optimal_temperature_min TINYINT COMMENT '最低适宜温度(℃)',
    optimal_temperature_max TINYINT COMMENT '最高适宜温度(℃)',
    ideal_humidity_min TINYINT COMMENT '最低适宜湿度(%)',
    ideal_humidity_max TINYINT COMMENT '最高适宜湿度(%)',
    watering_frequency_summer TINYINT COMMENT '夏季浇水频率(天)',
    watering_frequency_winter TINYINT COMMENT '冬季浇水频率(天)',
    fertilizing_frequency TINYINT COMMENT '施肥频率(天)',
    repotting_frequency TINYINT COMMENT '换盆频率(月)',
    description TEXT COMMENT '植物描述',
    care_tips TEXT COMMENT '养护技巧',
    common_problems TEXT COMMENT '常见问题',
    toxicity ENUM('无毒', '微毒', '有毒', '剧毒') DEFAULT '无毒',
    image_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 我的植物表
CREATE TABLE IF NOT EXISTS my_plants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    species_id INT NOT NULL,
    nickname VARCHAR(50) NOT NULL COMMENT '植物昵称',
    purchase_date DATE COMMENT '购买日期',
    purchase_source VARCHAR(100) COMMENT '购买来源',
    purchase_price DECIMAL(8,2) COMMENT '购买价格',
    location ENUM('客厅', '卧室', '阳台', '书房', '厨房', '卫生间', '办公室', '庭院') DEFAULT '客厅',
    specific_spot VARCHAR(100) COMMENT '具体位置',
    health_status ENUM('非常健康', '健康', '一般', '需关注', '生病', '濒危') DEFAULT '健康',
    growth_stage ENUM('幼苗', '生长期', '成熟期', '开花期', '结果期', '休眠期') DEFAULT '生长期',
    last_watered DATE,
    last_fertilized DATE,
    last_repotted DATE,
    last_pruned DATE,
    notes TEXT COMMENT '个性化备注',
    profile_image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES plant_species(id)
);

-- 养护记录表
CREATE TABLE IF NOT EXISTS care_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plant_id INT NOT NULL,
    care_type ENUM('浇水', '施肥', '换盆', '修剪', '除虫', '清洁叶片', '移动位置', '其他护理') NOT NULL,
    care_date DATETIME NOT NULL,
    details TEXT,
    amount_used VARCHAR(50) COMMENT '用量（如：500ml, 10g）',
    product_used VARCHAR(100) COMMENT '使用的产品',
    observed_effect ENUM('明显改善', '轻微改善', '无变化', '有不良反应') DEFAULT '无变化',
    notes TEXT COMMENT '观察记录',
    next_due_date DATE COMMENT '下次养护预计日期',
    FOREIGN KEY (plant_id) REFERENCES my_plants(id) ON DELETE CASCADE
);

-- 环境监测记录表
CREATE TABLE IF NOT EXISTS environment_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plant_id INT NOT NULL,
    log_date DATETIME NOT NULL,
    temperature DECIMAL(4,1) COMMENT '温度℃',
    humidity TINYINT COMMENT '湿度%',
    light_intensity INT COMMENT '光照强度(Lux)',
    soil_moisture TINYINT COMMENT '土壤湿度%',
    data_source ENUM('手动记录', '传感器', '天气API') DEFAULT '手动记录',
    notes TEXT,
    FOREIGN KEY (plant_id) REFERENCES my_plants(id) ON DELETE CASCADE
);

-- 生长记录表
CREATE TABLE IF NOT EXISTS growth_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plant_id INT NOT NULL,
    record_date DATE NOT NULL,
    height_cm DECIMAL(6,2) COMMENT '高度(cm)',
    width_cm DECIMAL(6,2) COMMENT '宽度(cm)',
    stem_diameter_mm DECIMAL(5,2) COMMENT '茎干直径(mm)',
    leaf_count INT COMMENT '叶片数量',
    new_leaf_count INT COMMENT '新叶数量',
    flower_count INT COMMENT '花朵数量',
    fruit_count INT COMMENT '果实数量',
    health_score TINYINT COMMENT '健康评分1-10',
    pest_problems BOOLEAN DEFAULT FALSE,
    disease_problems BOOLEAN DEFAULT FALSE,
    observations TEXT COMMENT '观察记录',
    image_path VARCHAR(500),
    FOREIGN KEY (plant_id) REFERENCES my_plants(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_plant_type ON plant_species(plant_type);
CREATE INDEX IF NOT EXISTS idx_difficulty ON plant_species(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_health_status ON my_plants(health_status);
CREATE INDEX IF NOT EXISTS idx_location ON my_plants(location);
CREATE INDEX IF NOT EXISTS idx_last_watered ON my_plants(last_watered);
CREATE INDEX IF NOT EXISTS idx_care_date ON care_logs(care_date);
CREATE INDEX IF NOT EXISTS idx_care_type ON care_logs(care_type);
CREATE INDEX IF NOT EXISTS idx_next_due ON care_logs(next_due_date);