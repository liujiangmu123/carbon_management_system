import os
import stat

# 项目根目录名称
PROJECT_NAME = "carbon_management_system"

# 定义项目结构
# (目录名, [文件名列表] 或 [ (子目录名, [孙文件名列表]), ... ] )
PROJECT_STRUCTURE = (
    PROJECT_NAME,
    [
        "main.py",  # 主应用程序入口
        "requirements.txt", # 项目依赖
        "README.md", # 项目说明
        (
            "config",  # 配置文件夹
            [
                "__init__.py",
                "settings.py",  # 应用配置，如API密钥、默认参数等
                "db_config.py",  # 数据库连接配置 (如果使用数据库)
                "logging_config.py", # 日志配置
            ],
        ),
        (
            "core",  # 核心业务逻辑和共享组件
            [
                "__init__.py",
                "base_model.py",  # 模型基类 (可选, 用于通用CRUD操作等)
                "base_controller.py",  # 控制器基类 (可选, 用于通用事件处理等)
                "base_view.py",  # 视图基类或窗口基类 (例如，自定义的QMainWindow)
                "app_signals.py", # 应用全局信号
            ],
        ),
        (
            "modules",  # 主要功能模块
            [
                "__init__.py",
                (
                    "system_management",  # 1. 系统基础与用户管理
                    [
                        "__init__.py",
                        "models.py",  # 用户、角色、权限、系统配置、审计日志等数据模型
                        "controllers.py",  # 用户认证、用户管理、角色管理、权限控制、系统配置管理、审计日志记录等逻辑
                        "services.py", # 更复杂的业务逻辑服务，如密码策略服务
                        (
                            "views",  # PyQt5 UI 文件转换后的 .py 文件或自定义视图类
                            [
                                "__init__.py",
                                "login_dialog.py",  # 登录对话框界面逻辑
                                "user_management_widget.py",  # 用户管理界面逻辑
                                "role_management_widget.py",  # 角色管理界面逻辑
                                "system_config_widget.py", # 系统配置界面逻辑
                                "audit_log_widget.py", # 审计日志查询界面逻辑
                            ],
                        ),
                        (
                            "widgets", # 该模块自定义的可复用PyQt5组件
                            [
                                "__init__.py",
                                "permission_tree_widget.py", # 权限树组件
                            ]
                        )
                    ],
                ),
                (
                    "data_acquisition",  # 2. 数据采集与管理
                    [
                        "__init__.py",
                        "models.py",  # 电厂、机组、燃料类型、活动数据、参数数据、支撑文档、数据校验规则等模型
                        "controllers.py",  # 数据录入、查询、校验、导入导出、文档关联等逻辑
                        "services.py", # 数据校验服务、数据聚合服务、外部数据源集成服务
                        (
                            "views",
                            [
                                "__init__.py",
                                "activity_data_form.py",  # 活动数据录入表单界面逻辑
                                "parameter_data_form.py",  # 参数数据录入表单界面逻辑
                                "data_query_widget.py",  # 数据查询与浏览界面逻辑
                                "document_management_widget.py", # 支撑文档管理界面逻辑
                                "data_validation_rule_widget.py", # 数据校验规则配置界面
                            ],
                        ),
                        (
                            "widgets",
                            [
                                "__init__.py",
                                "data_table_view.py", # 可配置的数据表格组件
                                "file_upload_widget.py", # 文件上传组件
                            ]
                        )
                    ],
                ),
                (
                    "emission_calculation",  # 3. 碳排放核算引擎
                    [
                        "__init__.py",
                        "models.py",  # 排放因子、计算公式定义、排放结果、计算日志等模型
                        "controllers.py",  # 触发核算任务、展示核算结果、管理排放因子等逻辑
                        "services.py",  # 核心CO2排放计算逻辑、排放因子选用逻辑、燃料参数处理逻辑
                        (
                            "views",
                            [
                                "__init__.py",
                                "emission_factor_manager_widget.py",  # 排放因子库管理界面逻辑
                                "calculation_task_widget.py",  # 排放核算任务界面逻辑
                                "emission_result_display_widget.py",  # 排放结果展示与分析界面逻辑
                            ],
                        ),
                        (
                            "widgets",
                            [
                                "__init__.py",
                                "formula_display_widget.py", # 计算公式展示组件
                            ]
                        )
                    ],
                ),
                (
                    "mrv_management",  # 4. 监测、报告与核查 (MRV) 管理
                    [
                        "__init__.py",
                        "models.py",  # DQCP、排放报告、核查记录、不符合项、合规日历任务等模型
                        "controllers.py",  # DQCP管理、报告生成与提交流程、核查支持、任务管理等逻辑
                        "services.py", # DQCP管理服务、排放报告生成服务、合规任务调度服务
                        (
                            "views",
                            [
                                "__init__.py",
                                "dqcp_editor_widget.py",  # DQCP创建/编辑界面逻辑
                                "emission_report_generator_widget.py",  # 年度排放报告生成界面逻辑
                                "verification_support_widget.py",  # 核查支持与不符合项管理界面逻辑
                                "compliance_calendar_widget.py", # 合规日历与任务管理界面逻辑
                            ],
                        ),
                        (
                            "widgets",
                            [
                                "__init__.py",
                                "rich_text_editor_widget.py", # 富文本编辑器 (用于DQCP等)
                            ]
                        )
                    ],
                ),
                (
                    "ets_management",  # 5. 碳排放权交易体系 (ETS) 管理
                    [
                        "__init__.py",
                        "models.py",  # 配额账户、配额分配基准线、调峰系数、交易记录、CCER记录、履约义务等模型
                        "controllers.py",  # 配额账户管理、市场交易记录、CCER管理、履约清缴辅助等逻辑
                        "services.py", # 配额核算服务、CCER抵消服务、履约管理服务
                        (
                            "views",
                            [
                                "__init__.py",
                                "allowance_account_dashboard.py",  # 配额账户总览仪表盘界面逻辑
                                "ets_benchmark_manager_widget.py", # 配额基准线管理界面逻辑
                                "ccer_inventory_widget.py",  # CCER库存管理界面逻辑
                                "compliance_surrender_workbench.py", # 履约清缴工作台界面逻辑
                                "allowance_transaction_ledger_widget.py", # 配额交易台账界面
                            ],
                        ),
                        (
                            "widgets",
                            [
                                "__init__.py",
                                "market_data_chart_widget.py", # 碳市场行情图表组件
                            ]
                        )
                    ],
                ),
                (
                    "ai_support",  # 6. AI 智能分析与决策支持
                    [
                        "__init__.py",
                        "models.py",  # AI模型元数据、预测结果、优化建议、场景分析记录等模型
                        "controllers.py",  # AI任务调度、结果展示、模型管理接口等逻辑
                        "services.py",  # 数据异常检测服务、预测性维护服务、效率优化服务、碳价预测服务、情景分析服务
                        (
                            "views",
                            [
                                "__init__.py",
                                "ai_analytics_dashboard.py",  # AI智能分析仪表盘界面逻辑
                                "anomaly_detection_workbench.py",  # 数据异常检测结果展示与处理界面逻辑
                                "carbon_price_forecast_widget.py", # 碳市场价格预测模块界面逻辑
                                "scenario_analysis_widget.py", # 情景模拟与What-if分析界面逻辑
                            ],
                        ),
                        (
                            "widgets",
                            [
                                "__init__.py",
                                "prediction_chart_widget.py", # 预测结果图表组件
                            ]
                        )
                    ],
                ),
            ],
        ),
        (
            "resources",  # 资源文件夹
            [
                "__init__.py", # 使其可以被导入，虽然通常不直接导入资源
                (
                    "icons",  # 图标
                    [
                        # 示例图标文件，实际项目中需要添加
                        # "app_icon.png",
                        # "open_file.svg",
                        # "save_file.svg",
                    ],
                ),
                (
                    "ui",  # Qt Designer .ui 文件 (如果使用Qt Designer)
                    [
                        # 示例 .ui 文件，实际项目中需要创建
                        # "login_dialog.ui",
                        # "main_window.ui",
                        # "user_management_widget.ui",
                    ],
                ),
                (
                    "templates",  # 报告模板、导入导出模板等
                    [
                        # "annual_emission_report_template.xlsx",
                        # "data_import_template_fuel.csv",
                    ],
                ),
                (
                    "styles", # QSS样式表文件
                    [
                        # "default_style.qss",
                    ]
                )
            ],
        ),
        (
            "utils",  # 工具类文件夹
            [
                "__init__.py",
                "logger_setup.py",  # 日志记录器设置
                "helpers.py",  # 通用辅助函数，如日期转换、文件操作等
                "validators.py",  # 数据校验函数/类
                "decorators.py", # 自定义装饰器，如权限检查
                "constants.py", # 项目中使用的常量
                "exceptions.py", # 自定义异常类
            ],
        ),
        (
            "tests",  # 测试文件夹
            [
                "__init__.py",
                # "test_system_management_models.py",
                # "test_system_management_controllers.py",
                # "test_data_acquisition_services.py",
                # ... (每个模块都可以有自己的测试文件)
            ],
        ),
    ],
)

# Python 文件头部注释和基本导入
PYTHON_FILE_HEADER = """# -*- coding: utf-8 -*-
# @Time    : {creation_time}
# @Author  : Your Name / Company Name
# @Email   : your.email@example.com
# @File    : {file_name}
# @Software: PyCharm / VSCode
# @Description: {description}

# Python 标准库导入
import sys
import os

# PyQt5 相关导入 (根据实际需要调整)
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
# from PyQt5.QtCore import Qt, pyqtSignal, QObject

# 项目内部模块导入 (示例)
# from ..core.base_controller import BaseController
# from ...utils.logger_setup import logger

"""

# 文件描述映射
FILE_DESCRIPTIONS = {
    "main.py": "应用程序的主入口点，负责初始化和启动整个应用。",
    "requirements.txt": "列出项目运行所需的所有Python依赖包及其版本。",
    "README.md": "项目说明文件，包含项目简介、安装指南、使用方法等。",
    # config
    "config/__init__.py": "将 config 目录标记为Python包。",
    "config/settings.py": "存储应用程序的全局配置项，例如API密钥、默认路径、外部服务URL等。",
    "config/db_config.py": "存储数据库连接相关的配置信息，如主机、端口、用户名、密码、数据库名等。",
    "config/logging_config.py": "配置应用程序的日志记录行为，如日志级别、格式、输出目标等。",
    # core
    "core/__init__.py": "将 core 目录标记为Python包。",
    "core/base_model.py": "提供数据模型类的基类，可能包含通用的数据库操作方法或属性。",
    "core/base_controller.py": "提供控制器类的基类，可能包含通用的事件处理逻辑或与视图、模型的交互接口。",
    "core/base_view.py": "提供视图类（如窗口、对话框）的基类，可能包含通用的UI设置或布局方法。",
    "core/app_signals.py": "定义应用级别的全局信号，用于不同模块间的解耦通信。",
    # utils
    "utils/__init__.py": "将 utils 目录标记为Python包。",
    "utils/logger_setup.py": "初始化和配置项目日志记录器。",
    "utils/helpers.py": "包含项目中通用的辅助函数，如日期时间处理、文件操作、数据格式化等。",
    "utils/validators.py": "包含用于数据校验的函数或类，确保输入数据的有效性和一致性。",
    "utils/decorators.py": "定义项目中可复用的装饰器，例如用于权限检查、日志记录、性能分析等。",
    "utils/constants.py": "定义项目中使用的全局常量，如枚举值、固定字符串、配置键名等。",
    "utils/exceptions.py": "定义项目中自定义的异常类，用于更精确地处理特定错误情况。",
    # resources
    "resources/__init__.py": "将 resources 目录标记为Python包。",
    "resources/icons/__init__.py": "图标子目录的包标记。",
    "resources/ui/__init__.py": "UI文件子目录的包标记。",
    "resources/templates/__init__.py": "模板文件子目录的包标记。",
    "resources/styles/__init__.py": "样式文件子目录的包标记。",
    # tests
    "tests/__init__.py": "将 tests 目录标记为Python包。",
    # modules - common
    "modules/__init__.py": "将 modules 目录标记为Python包。",
}

# 为模块内部文件生成描述
MODULE_FILE_TEMPLATES = {
    "__init__.py": "将 {module_name} 模块声明为Python包。",
    "models.py": "定义 {module_name} 模块的数据模型 (例如，与数据库表对应的类，或业务对象类)。",
    "controllers.py": "实现 {module_name} 模块的业务逻辑和流程控制，协调模型和视图。",
    "services.py": "提供 {module_name} 模块中更复杂或可复用的业务服务逻辑。",
    "views/__init__.py": "将 {module_name} 模块的 views 子目录标记为Python包。",
    "widgets/__init__.py": "将 {module_name} 模块的 widgets 子目录标记为Python包。",
}

MODULE_VIEW_FILE_TEMPLATES = {
    "login_dialog.py": "系统登录对话框的界面逻辑和事件处理。",
    "user_management_widget.py": "用户管理界面的UI元素、数据展示和用户交互逻辑。",
    "role_management_widget.py": "角色管理界面的UI元素、数据展示和用户交互逻辑。",
    "system_config_widget.py": "系统配置项展示与编辑界面的逻辑。",
    "audit_log_widget.py": "审计日志查询与展示界面的逻辑。",
    "activity_data_form.py": "活动数据（如燃料消耗、发电量）录入表单的界面逻辑。",
    "parameter_data_form.py": "参数数据（如煤质参数）录入表单的界面逻辑。",
    "data_query_widget.py": "提供数据查询、筛选和浏览功能的界面逻辑。",
    "document_management_widget.py": "支撑文档上传、下载、关联和管理的界面逻辑。",
    "data_validation_rule_widget.py": "数据校验规则定义与管理的界面逻辑。",
    "emission_factor_manager_widget.py": "排放因子库的查看、编辑和管理界面逻辑。",
    "calculation_task_widget.py": "碳排放核算任务的发起、监控和结果初步展示界面逻辑。",
    "emission_result_display_widget.py": "碳排放核算结果的详细展示、分析图表和追溯界面逻辑。",
    "dqcp_editor_widget.py": "数据质量控制计划（DQCP）的在线编辑、版本管理和审批流程界面逻辑。",
    "emission_report_generator_widget.py": "年度/月度排放报告的自动生成、预览、编辑和导出界面逻辑。",
    "verification_support_widget.py": "支持第三方核查工作的界面，包括数据提供、不符合项跟踪与整改管理。",
    "compliance_calendar_widget.py": "合规日历任务展示、提醒和管理界面逻辑。",
    "allowance_account_dashboard.py": "碳配额账户总览仪表盘，展示配额、交易、盈亏等信息。",
    "ets_benchmark_manager_widget.py": "碳排放配额分配基准线数据的管理界面。",
    "ccer_inventory_widget.py": "国家核证自愿减排量（CCER）库存管理和抵销申请界面逻辑。",
    "compliance_surrender_workbench.py": "年度履约清缴工作台，辅助制定履约策略和记录操作。",
    "allowance_transaction_ledger_widget.py": "碳配额交易台账，记录和查询所有配额交易。",
    "ai_analytics_dashboard.py": "AI智能分析结果的综合仪表盘展示界面。",
    "anomaly_detection_workbench.py": "数据显示质量异常检测结果的展示、确认和处理工作台界面。",
    "carbon_price_forecast_widget.py": "碳市场价格预测结果的展示和分析界面。",
    "scenario_analysis_widget.py": "What-if情景模拟的参数配置、执行和结果对比分析界面。",
}

MODULE_WIDGET_FILE_TEMPLATES = {
    "permission_tree_widget.py": "{module_name} 模块中用于展示和选择权限的树形组件。",
    "data_table_view.py": "{module_name} 模块中通用的、可配置的数据展示表格组件。",
    "file_upload_widget.py": "{module_name} 模块中用于文件上传的自定义组件。",
    "formula_display_widget.py": "{module_name} 模块中用于美观展示计算公式的组件。",
    "rich_text_editor_widget.py": "{module_name} 模块中用于富文本编辑的组件 (例如，用于DQCP文档编辑)。",
    "market_data_chart_widget.py": "{module_name} 模块中用于展示碳市场行情数据的图表组件。",
    "prediction_chart_widget.py": "{module_name} 模块中用于展示AI预测结果（如趋势、置信区间）的图表组件。",
}


def create_project_structure(base_path, structure, module_context=""):
    """
    递归创建项目结构。
    :param base_path: 当前基础路径
    :param structure: 当前级别的结构定义 (元组或列表)
    :param module_context: 当前模块的名称上下文 (用于生成描述)
    """
    from datetime import datetime

    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name = structure[0]
    path = os.path.join(base_path, name)

    if isinstance(structure[1], list):  # 如果是目录
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"创建目录: {path}")

        for item in structure[1]:
            if isinstance(item, str):  # 如果是文件
                file_path = os.path.join(path, item)
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        relative_file_path = os.path.join(name if name != PROJECT_NAME else "", item).replace("\\", "/") # 用于描述
                        if module_context and path.startswith(os.path.join(PROJECT_NAME, "modules")): # 模块内部文件
                            module_name_for_desc = module_context.split('/')[-1] # 获取当前模块名
                            current_dir_name = os.path.basename(path) # views, widgets

                            desc_key_short = item # e.g. login_dialog.py
                            desc_key_long = f"{current_dir_name}/{item}" # e.g. views/login_dialog.py

                            if desc_key_long in MODULE_VIEW_FILE_TEMPLATES:
                                description = MODULE_VIEW_FILE_TEMPLATES[desc_key_long]
                            elif desc_key_short in MODULE_VIEW_FILE_TEMPLATES and current_dir_name == "views":
                                description = MODULE_VIEW_FILE_TEMPLATES[desc_key_short]
                            elif desc_key_long in MODULE_WIDGET_FILE_TEMPLATES:
                                description = MODULE_WIDGET_FILE_TEMPLATES[desc_key_long].format(module_name=module_name_for_desc)
                            elif desc_key_short in MODULE_WIDGET_FILE_TEMPLATES and current_dir_name == "widgets":
                                description = MODULE_WIDGET_FILE_TEMPLATES[desc_key_short].format(module_name=module_name_for_desc)
                            elif item in MODULE_FILE_TEMPLATES:
                                description = MODULE_FILE_TEMPLATES[item].format(module_name=module_name_for_desc)
                            else:
                                description = f"{module_name_for_desc} 模块的 {item} 文件。"

                        elif relative_file_path in FILE_DESCRIPTIONS:
                            description = FILE_DESCRIPTIONS[relative_file_path]
                        else: # fallback for module files not explicitly listed
                            clean_path = path.replace(PROJECT_NAME + os.sep, "")
                            path_parts = clean_path.split(os.sep)
                            if "modules" in path_parts:
                                module_idx = path_parts.index("modules")
                                if module_idx + 1 < len(path_parts):
                                    current_module_name = path_parts[module_idx+1]
                                    if item in MODULE_FILE_TEMPLATES:
                                        description = MODULE_FILE_TEMPLATES[item].format(module_name=current_module_name)
                                    else:
                                        description = f"{current_module_name} 模块的 {item} 文件。"
                                else:
                                    description = f"{item} 文件。"

                            else:
                                description = f"{item} 文件。"


                        if item.endswith(".py"):
                            f.write(
                                PYTHON_FILE_HEADER.format(
                                    creation_time=current_time_str,
                                    file_name=item,
                                    description=description,
                                )
                            )
                            if item == "main.py":
                                f.write("\n\n")
                                f.write("def main():\n")
                                f.write("    # 主程序逻辑开始\n")
                                f.write("    print(\"发电厂碳管理软件启动中...\")\n")
                                f.write("    # app = QApplication(sys.argv)\n")
                                f.write("    # # 加载主窗口等\n")
                                f.write("    # # ex = MainWindow()\n")
                                f.write("    # # ex.show()\n")
                                f.write("    # # sys.exit(app.exec_())\n")
                                f.write("    print(\"请在此处实现PyQt5应用初始化和主循环。\")\n\n")
                                f.write("if __name__ == '__main__':\n")
                                f.write("    main()\n")
                            elif item == "requirements.txt":
                                f.write("PyQt5>=5.15.0\n")
                                f.write("# pandas>=1.0.0  # 如果需要处理表格数据\n")
                                f.write("# openpyxl>=3.0.0 # 如果需要读写xlsx文件\n")
                                f.write("# requests>=2.0.0 # 如果需要进行HTTP请求\n")
                                f.write("# matplotlib>=3.0.0 # 如果需要绘图\n")
                                f.write("# scikit-learn>=0.24 # 如果AI模块使用sklearn\n")
                                f.write("# tensorflow>=2.0 # 或 pytorch, 如果AI模块使用深度学习\n")
                            elif item == "README.md":
                                f.write(f"# {PROJECT_NAME}\n\n")
                                f.write("发电厂碳管理软件项目。\n\n")
                                f.write("## 项目简介\n\n")
                                f.write("本项目旨在为发电企业提供一套全面的碳排放管理解决方案，涵盖数据采集、碳核算、MRV管理、ETS交易支持以及AI智能分析等功能。\n\n")
                                f.write("## 技术栈\n\n")
                                f.write("- Python\n")
                                f.write("- PyQt5 (GUI)\n\n")
                                f.write("## 安装与运行\n\n")
                                f.write("1. 克隆项目到本地。\n")
                                f.write("2. 创建并激活Python虚拟环境。\n")
                                f.write("   ```bash\n")
                                f.write("   python -m venv venv\n")
                                f.write("   # Windows\n")
                                f.write("   venv\\Scripts\\activate\n")
                                f.write("   # macOS/Linux\n")
                                f.write("   source venv/bin/activate\n")
                                f.write("   ```\n")
                                f.write("3. 安装依赖：\n")
                                f.write("   ```bash\n")
                                f.write("   pip install -r requirements.txt\n")
                                f.write("   ```\n")
                                f.write("4. 运行主程序：\n")
                                f.write("   ```bash\n")
                                f.write("   python main.py\n")
                                f.write("   ```\n\n")
                                f.write("## 目录结构说明\n\n")
                                f.write("详细的目录结构请参见项目内部文件或设计文档。\n")

                            else:
                                f.write("\npass # 请在此处实现具体功能\n")
                        elif item.endswith(".ui"):
                             f.write("\n")
                             f.write("\n")
                        elif item.endswith(".qss"):
                             f.write("/* 这是一个空的 .qss 文件占位符 */\n")
                             f.write("/* 请在此处编写Qt样式表 */\n")

                    print(f"创建文件: {file_path}")
            elif isinstance(item, tuple):  # 如果是子目录
                new_module_context = module_context
                # 更新模块上下文，特别是进入 'modules' 的子目录时
                if name == "modules":
                    new_module_context = item[0] # item[0] is the module name like 'system_management'
                elif module_context and name in ["views", "widgets"]: # if we are already in a module and going into views/widgets
                    new_module_context = f"{module_context}/{name}"


                create_project_structure(path, item, new_module_context)
    else: # 理论上顶层应该是目录
        pass


if __name__ == "__main__":
    # 在当前脚本所在目录下创建项目
    project_base_path = os.getcwd()
    # project_root_path = os.path.join(project_base_path, PROJECT_NAME) # 这会导致项目在项目内部创建

    # 确保项目根目录在当前工作目录的下一级
    # 如果PROJECT_STRUCTURE的第一个元素就是项目名，则base_path应该是getcwd()
    # create_project_structure的第一个参数是其父目录
    create_project_structure(project_base_path, PROJECT_STRUCTURE)

    print(f"\n项目 '{PROJECT_NAME}' 结构生成完毕！")
    print(f"项目路径: {os.path.join(project_base_path, PROJECT_NAME)}")
    print("请检查生成的目录和文件，并开始您的开发工作。")
    print("建议使用VSCode打开生成的项目文件夹。")
    print("对于 .ui 文件, 您需要使用 Qt Designer 进行设计, 然后可以使用 pyuic5 工具将其转换为 .py 文件。")
    print("例如: pyuic5 -x input.ui -o output.py")

