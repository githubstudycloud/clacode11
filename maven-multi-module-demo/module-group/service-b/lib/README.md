# module-group/service-b - 本地Jar依赖说明

## 依赖清单

| Jar文件 | GroupId | ArtifactId | Version | 说明 |
|---------|---------|------------|---------|------|
| gson-2.8.5.jar | com.google.code.gson | gson | 2.8.5 | Google Gson - Service B专用 |

## 使用说明

这些jar文件通过maven-install-plugin在构建时自动安装到本地Maven仓库。

### 构建时自动安装

```bash
mvn clean install
```

### 验证依赖

```bash
mvn dependency:tree
```

## 注意事项

1. 这些jar文件已提交到Git仓库
2. 构建时会自动处理，无需手动安装
3. Jenkins构建时也会自动处理

## 更新历史

- 由 lib_manager.py 自动生成
