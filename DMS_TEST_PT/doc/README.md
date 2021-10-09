## 目录结构
    ├── _library        // 框架基础底层搭建的代码，除框架开发同学外，其他同学无需关心
    │    ├── global_valule.py     // 全局变量    
    │    ├── json_lib.py     // json数据转换、提取相关参数
    │    ├── log.py     // 基础日志管理
    │    └── sys.py     // 框架基础能力函数库
    │
    ├── config
    │    └── config.py        // 内部配置文件
    │
    ├── library
    │    ├── adb_lib.py      // adb相关操作，包括由os向J2发送指令
    │    ├── common_lib.py       // 集成library库内所有方法
    │    ├── serial_lib.py       // 串口相关操作
    │    └── uiautomator_lib.py      //UI相关操作
    │
    ├── modules
    │    └── mcu_related        // 模块名称
    │    │     ├── testcase       // 模块下testcase存放的目录
    │    │     ├── pylib         // 模块下case所用接口存放的文件
    │    │     └── conftest.py      //模块级别setup、teardown存放的文件
    │    ├── bpu_manage_test       // 模块名称
    │    └── conftest.py        // 全局setup、teardown存放的文件
    │
    ├── result
    │    ├── log        // 日志存放目录
    │    ├── reports       // 测试报告存放目录
    │    └── uiautomator        // UI相关文件存放目录
    │
    ├── tools
    │    ├── allure        // allure工具
    │    ├── allure_serve_start.py       // 生成测试报告
    │    └── pt_run.py        // 批量运行测试用例并生成报告
    │
    ├── variables
    │    └── ${cartype}_variable.py        // ${cartype}的资源文件（包含UI定位符、page activity）
    │
    ├── pytest.ini      // pytest配置文件。用户配置写在这里。
    │
    └── README.md        // help