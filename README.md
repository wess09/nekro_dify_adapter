# NekroDify - Dify 适配器插件

一个用于 NekroAgent 的 Dify 工作流适配器插件，允许通过 Dify API 调用 Dify 工作流。

## 功能特性

- 🔗 通过 Dify API 调用工作流
- ⚙️ 支持自定义 API 密钥和基础 URL
- 🔄 支持阻塞模式的工作流执行
- 📝 详细的日志记录和错误处理
- 🛠️ 简单易用的配置界面


## 配置

在插件配置界面中设置以下参数：

- **Dify API密钥**: 您的 Dify API 密钥，格式为 `app-xxxxxxxx`
- **Dify API基础URL**: Dify API 的基础 URL（默认：`https://api.dify.ai/v1`）
- **默认用户标识**: 默认的用户标识（默认：`nekro-agent-user`）


### 参数说明

- `inputs`: 工作流的输入参数，字典格式
- `user`: 可选的用户标识，用于区分不同用户的请求

## 人设配置

为了让 AI 能够正确使用这个工具，请在您的人设中添加工具描述

## 错误处理

插件包含完善的错误处理机制：

- API 密钥未配置时会提示用户设置
- API 调用失败时会返回详细的错误信息
- 所有操作都有详细的日志记录

## 开发信息

- **作者**: wess09
- **版本**: 1.0.2
- **仓库**: https://github.com/wess09/nekro_plugin_dify

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个插件！