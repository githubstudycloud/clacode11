# Maven多模块项目 - 练习题集

## 📝 使用说明

每个练习题都有：
- 📋 题目描述
- 🎯 学习目标
- 💡 提示
- ⭐ 难度等级（1-5星）
- ⏱️ 预计时间

**答案文件**: [EXERCISES_ANSWERS.md](EXERCISES_ANSWERS.md)

---

## 第1章: Maven基础练习

### 练习1.1: 理解Maven坐标 ⭐
**时间**: 10分钟

**题目**:
以下Maven坐标的含义是什么？
```xml
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-web</artifactId>
<version>2.7.18</version>
```

**问题**:
1. groupId代表什么？
2. artifactId代表什么？
3. version中的 `.18` 是什么意思？
4. 这个依赖的完整坐标是什么？

### 练习1.2: 创建简单POM ⭐⭐
**时间**: 15分钟

**题目**:
手动创建一个最简单的Maven项目POM文件，要求：
- groupId: com.student
- artifactId: my-first-maven
- version: 1.0.0
- packaging: jar
- Java版本: 1.8

### 练习1.3: 理解生命周期 ⭐⭐
**时间**: 15分钟

**题目**:
执行以下命令会发生什么？按顺序列出执行的阶段。
```bash
mvn clean install
```

**问题**:
1. clean阶段做了什么？
2. install之前会执行哪些阶段？
3. 最终生成的文件在哪里？

---

## 第2章: 多模块项目练习

### 练习2.1: 创建父子项目 ⭐⭐⭐
**时间**: 30分钟

**题目**:
创建一个包含1个父项目和2个子模块的Maven多模块项目。

**要求**:
- 父项目: student-project
- 子模块1: utils (工具类)
- 子模块2: app (应用)
- app 依赖 utils
- 使用Java 11

**提示**:
1. 父POM的packaging是什么？
2. 如何声明子模块？
3. 子模块如何继承父POM？

### 练习2.2: 配置依赖管理 ⭐⭐⭐
**时间**: 20分钟

**题目**:
在父POM中配置 `dependencyManagement`，统一管理以下依赖的版本：
- JUnit: 4.13.2
- Lombok: 1.18.24
- Guava: 31.1-jre

然后在子模块中使用这些依赖（不指定版本）。

### 练习2.3: 依赖传递实验 ⭐⭐⭐
**时间**: 25分钟

**题目**:
创建三个模块的依赖链：
```
module-c → module-b → module-a
```

**要求**:
1. module-a 中添加 commons-lang3 依赖
2. module-b 依赖 module-a
3. module-c 依赖 module-b
4. 验证 module-c 是否可以使用 commons-lang3 的类

**问题**:
- 依赖的scope对传递有什么影响？

---

## 第3章: Spring Boot集成练习

### 练习3.1: 创建Spring Boot模块 ⭐⭐⭐
**时间**: 35分钟

**题目**:
在多模块项目中创建一个Spring Boot Web服务。

**要求**:
1. 模块名: web-service
2. 端口: 9000
3. 提供 `/api/info` 接口，返回服务信息（JSON格式）
4. 提供 `/api/time` 接口，返回当前时间

**提示**:
- 需要配置 spring-boot-maven-plugin
- 使用 @RestController
- 在 application.yml 配置端口

### 练习3.2: 模块间调用 ⭐⭐⭐⭐
**时间**: 45分钟

**题目**:
创建一个多模块Spring Boot项目：
- common: 公共工具模块
- user-service: 用户服务 (8081)
- order-service: 订单服务 (8082)

**要求**:
1. common模块提供 `UserUtil` 工具类
2. user-service 使用 common 中的工具类
3. order-service 也使用 common 中的工具类
4. 两个服务都能正常启动

**问题**:
- common模块需要配置 spring-boot-maven-plugin 吗？
- 为什么？

---

## 第4章: 本地jar依赖练习

### 练习4.1: 手动安装jar ⭐⭐
**时间**: 15分钟

**题目**:
下载 `commons-io-2.11.0.jar` 并手动安装到本地Maven仓库。

**要求**:
1. 使用 `mvn install:install-file` 命令
2. groupId: commons-io
3. artifactId: commons-io
4. version: 2.11.0

**验证**:
创建一个项目引用这个依赖，确认可以正常使用。

### 练习4.2: 配置maven-install-plugin ⭐⭐⭐
**时间**: 30分钟

**题目**:
为项目的 common 模块添加本地jar自动安装功能。

**要求**:
1. 创建 `common/lib` 目录
2. 放入 `guava-28.0-jre.jar`
3. 配置 maven-install-plugin
4. 在POM中正常声明依赖
5. 验证构建成功

**提示**:
- 使用 `${project.basedir}/lib/guava-28.0-jre.jar`
- phase: validate
- goal: install-file
- generatePom: true

### 练习4.3: 使用lib_manager工具 ⭐⭐⭐⭐
**时间**: 40分钟

**题目**:
使用 `lib_manager.py` 工具为多个模块配置本地jar依赖。

**场景**:
- common模块: commons-lang3, guava
- service-a模块: fastjson
- service-b模块: gson

**要求**:
1. 准备jar文件
2. 编写配置文件 `jars-config.yaml`
3. 运行工具
4. 应用生成的配置
5. 验证构建成功

### 练习4.4: 依赖冲突解决 ⭐⭐⭐⭐⭐
**时间**: 50分钟

**题目**:
故意制造一个依赖冲突并解决它。

**场景**:
- module-a 依赖 guava 28.0
- module-b 依赖 guava 30.0
- module-c 同时依赖 module-a 和 module-b

**问题**:
1. 会使用哪个版本的guava？
2. 如何强制使用指定版本？
3. 如何排除某个传递依赖？

**提示**:
- 使用 `mvn dependency:tree` 查看
- 使用 `<exclusions>` 排除
- 在 `dependencyManagement` 中强制版本

---

## 第5章: 构建和测试练习

### 练习5.1: 编写单元测试 ⭐⭐⭐
**时间**: 30分钟

**题目**:
为 common 模块的工具类编写单元测试。

**要求**:
1. 测试类: `CommonUtilTest`
2. 至少3个测试方法
3. 使用 JUnit 4
4. 测试覆盖率 > 80%

**示例**:
```java
@Test
public void testGreet() {
    String result = CommonUtil.greet("Alice");
    assertTrue(result.contains("Alice"));
}
```

### 练习5.2: 配置测试跳过 ⭐⭐
**时间**: 15分钟

**题目**:
配置Maven允许在快速构建时跳过测试。

**要求**:
1. 命令行跳过测试
2. 通过profile配置
3. 在POM中配置默认行为

### 练习5.3: 集成测试配置 ⭐⭐⭐⭐
**时间**: 45分钟

**题目**:
为Spring Boot服务配置集成测试。

**要求**:
1. 创建 `@SpringBootTest` 测试类
2. 测试 REST API
3. 使用 `TestRestTemplate`
4. 验证返回结果

**示例**:
```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
public class ControllerIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void testHelloEndpoint() {
        String response = restTemplate.getForObject("/api/hello", String.class);
        assertNotNull(response);
    }
}
```

---

## 第6章: CI/CD练习

### 练习6.1: 编写Jenkinsfile ⭐⭐⭐
**时间**: 30分钟

**题目**:
为项目编写基本的Jenkinsfile。

**要求**:
1. 定义Maven和JDK工具
2. Checkout阶段
3. Build阶段
4. Test阶段
5. Archive阶段

### 练习6.2: 优化构建速度 ⭐⭐⭐⭐
**时间**: 40分钟

**题目**:
优化Maven构建速度。

**任务**:
1. 测量当前构建时间
2. 使用并行构建 (`-T` 参数)
3. 配置依赖缓存
4. 对比优化前后的时间

**问题**:
- 并行构建有什么限制？
- 什么情况下不能并行？

### 练习6.3: 自动化测试报告 ⭐⭐⭐⭐
**时间**: 45分钟

**题目**:
使用 `test-runner.py` 工具生成测试报告。

**要求**:
1. 运行完整测试套件
2. 生成HTML报告
3. 生成Markdown报告
4. 分析测试结果

---

## 第7章: 实战项目

### 项目7.1: 图书管理系统 ⭐⭐⭐⭐
**时间**: 2-3小时

**需求**:
开发一个简单的图书管理系统。

**模块设计**:
```
library-system/
├── common/              # 公共模块
├── book-service/        # 图书服务
└── user-service/        # 用户服务
```

**功能要求**:

**common模块**:
- 实体类: Book, User
- 工具类: DateUtil, StringUtil

**book-service**:
- 端口: 8081
- API:
  - GET /api/books - 获取所有图书
  - GET /api/books/{id} - 获取指定图书
  - POST /api/books - 添加图书
  - PUT /api/books/{id} - 更新图书
  - DELETE /api/books/{id} - 删除图书

**user-service**:
- 端口: 8082
- API:
  - GET /api/users - 获取所有用户
  - GET /api/users/{id} - 获取指定用户
  - POST /api/users - 添加用户

**技术要求**:
- 使用Spring Boot
- 使用内存存储（Map）
- 添加单元测试
- 编写README文档

**加分项**:
- 使用本地jar依赖（如 fastjson）
- 配置Jenkinsfile
- 生成API文档

### 项目7.2: 电商系统 ⭐⭐⭐⭐⭐
**时间**: 4-6小时

**需求**:
开发一个完整的电商系统后端。

**模块设计**:
```
ecommerce-system/
├── common/              # 公共模块
├── user-service/        # 用户服务
├── product-service/     # 商品服务
├── order-service/       # 订单服务
├── payment-service/     # 支付服务
└── gateway/            # API网关（可选）
```

**功能要求**:

**1. 用户服务 (8081)**
- 用户注册
- 用户登录
- 个人信息管理
- 收货地址管理

**2. 商品服务 (8082)**
- 商品分类
- 商品列表
- 商品详情
- 库存管理

**3. 订单服务 (8083)**
- 创建订单
- 订单列表
- 订单详情
- 订单状态管理

**4. 支付服务 (8084)**
- 模拟支付
- 支付回调
- 支付状态查询

**技术要求**:
- Spring Boot 2.7+
- Maven多模块
- RESTful API
- 单元测试覆盖率 > 60%
- 集成测试
- 本地jar依赖管理

**数据存储**:
- 使用内存Map
- 或使用H2数据库

**文档要求**:
- README.md
- API文档
- 架构设计文档
- 部署文档

**CI/CD要求**:
- Jenkinsfile
- 自动化测试
- 构建优化

---

## 第8章: 挑战题

### 挑战8.1: 性能优化 ⭐⭐⭐⭐⭐
**时间**: 2小时

**题目**:
优化一个慢速Maven项目的构建时间。

**初始状态**:
- 10个模块
- 每个模块有大量测试
- 构建时间: 15分钟

**目标**:
- 将构建时间降低到5分钟以内

**可用手段**:
- 并行构建
- 依赖缓存
- 测试优化
- 插件配置

### 挑战8.2: 依赖地狱 ⭐⭐⭐⭐⭐
**时间**: 2小时

**题目**:
解决一个复杂的依赖冲突问题。

**场景**:
项目有5个模块，每个模块依赖不同版本的：
- Jackson (2.10.x 到 2.13.x)
- Guava (28.x 到 31.x)
- Commons-Lang (3.8 到 3.12)

**要求**:
1. 分析依赖树
2. 找出所有冲突
3. 统一版本
4. 验证兼容性

### 挑战8.3: 自动化一切 ⭐⭐⭐⭐⭐
**时间**: 3小时

**题目**:
创建一个完全自动化的项目工作流。

**要求**:
1. 一键创建新项目
2. 自动生成代码框架
3. 自动配置依赖
4. 自动运行测试
5. 自动生成文档
6. 自动部署到本地环境

**工具**:
- Python脚本
- Maven插件
- Shell脚本
- Docker（可选）

---

## 附录: 练习评分标准

### 基础练习 (1-2星)
- 完成即可 (60分)
- 代码规范 (20分)
- 文档清晰 (20分)

### 中级练习 (3星)
- 功能完整 (50分)
- 代码质量 (20分)
- 测试覆盖 (15分)
- 文档完善 (15分)

### 高级练习 (4星)
- 功能完整 (40分)
- 代码质量 (25分)
- 测试覆盖 (20分)
- 性能优化 (10分)
- 文档完善 (5分)

### 挑战练习 (5星)
- 问题解决 (35分)
- 技术深度 (25分)
- 创新方案 (20分)
- 代码质量 (10分)
- 文档完善 (10分)

---

## 提交要求

### 代码提交
```bash
# 创建Git仓库
git init
git add .
git commit -m "Complete exercise X.X"

# 推送到远程（如GitHub）
git remote add origin <your-repo-url>
git push -u origin master
```

### 文档要求

每个练习需要提交：

1. **README.md** - 项目说明
2. **源代码** - 完整可运行
3. **测试报告** - 如适用
4. **问题记录** - 遇到的问题和解决方案

### 检查清单

提交前检查：
- [ ] 代码可以编译
- [ ] 测试可以通过
- [ ] 文档完整
- [ ] 没有硬编码路径
- [ ] .gitignore正确配置
- [ ] README清晰易懂

---

## 获取帮助

### 遇到问题时

1. **查看文档**: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)
2. **查看答案**: [EXERCISES_ANSWERS.md](EXERCISES_ANSWERS.md) (但要先自己尝试!)
3. **运行测试工具**: `python tools/test-runner.py`
4. **检查构建日志**: `mvn clean install -X`

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 找不到依赖 | 检查仓库配置和依赖声明 |
| 编译失败 | 查看错误信息，检查Java版本 |
| 测试失败 | 查看测试日志，逐个修复 |
| 构建慢 | 使用并行构建、跳过测试 |

---

## 学习建议

1. **按顺序完成**: 先做基础题，再做高级题
2. **理解原理**: 不要只是复制代码
3. **写文档**: 记录学习过程
4. **多练习**: 熟能生巧
5. **参考答案**: 但要理解为什么这样写

**祝你学习顺利！** 🎓
