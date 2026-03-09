# Consilium Guard | 安全守护

<img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=flat-square" alt="OpenClaw Skill">
<img src="https://img.shields.io/badge/Focus-Safety-red?style=flat-square" alt="Focus: Safety">

让 OpenClaw 不再鲁莽行事。在删除文件、调用 API、修改配置等危险操作前，强制进行多方审议。

## 为什么需要它

> "AI Agent 失控，向用户发送了 500 条垃圾消息" —— 这不是科幻，这是真实事故。

OpenClaw 很强大，但默认没有刹车。Consilium Guard 就是你的安全刹车。

## 它能拦截什么

| 操作 | 风险 | 守护动作 |
|------|------|----------|
| `rm -rf` / 删除文件 | 误删重要数据 | ⚠️ 拦截，要求确认 |
| 发送邮件/消息 | 信息泄露、骚扰 | ⚠️ 审查内容，限制频率 |
| 外部 API 调用 | 密钥泄露、费用失控 | ⚠️ 确认必要性和成本 |
| 修改系统配置 | 系统损坏 | ⚠️ 备份后再执行 |
| 访问敏感文件 | 隐私泄露 | ⚠️ 脱敏处理 |

## 工作原理

```
User: "删除所有临时文件"
     ↓
[Guardian 拦截]
     ↓
[PM] 用户想释放空间 → 但"临时"定义模糊
[Tech] 建议排除7天内访问的文件
[Security] ⚠️ 需确认具体目录
     ↓
[Decision] 询问用户: /tmp/ 还是 ~/.cache/ 还是指定路径?
```

## 快速开始

```bash
# 安装
openclaw skill install consilium-guard

# 配置 API Key
export DEEPSEEK_API_KEY="your-key"
# 或
export OPENAI_API_KEY="your-key"
```

## 使用

Guard 会自动拦截危险操作，无需手动调用：

```
You: 删除 logs 文件夹
OpenClaw: [Guardian] 即将删除 logs/，其中包含 156 个文件。
          建议先备份到 logs_backup_20240309/ 再删除？
          [确认] [查看文件列表] [取消]
```

## 配置

```bash
# 安全级别
export CONSILIUM_SAFETY_LEVEL=high    # 严格模式（推荐）
export CONSILIUM_SAFETY_LEVEL=medium  # 平衡模式
export CONSILIUM_SAFETY_LEVEL=low     # 快速模式

# 审议速度
export CONSILIUM_MODE=fast     # 轻量审议（3-5秒）
export CONSILIUM_MODE=standard # 标准审议（10-15秒）
export CONSILIUM_MODE=deep     # 深度审议（30秒+）
```

## 示例场景

### 文件删除
**User**: "清理磁盘空间"
**Without Guard**: AI 可能误删系统文件
**With Guard**: 
- 识别可安全删除的类别（缓存、日志、临时文件）
- 排除系统关键目录
- 建议先压缩备份

### API 调用
**User**: "分析这个网站"
**Without Guard**: AI 可能疯狂调用 API，费用爆炸
**With Guard**:
- 估算调用次数和成本
- 设置调用上限
- 建议缓存结果

### 数据导出
**User**: "导出所有邮件"
**Without Guard**: 可能包含敏感信息
**With Guard**:
- 扫描敏感内容
- 建议脱敏或加密
- 确认接收方身份

## 高级：自定义规则

创建 `~/.consilium/guard-rules.json`:

```json
{
  "blocked_patterns": ["*.key", "*.pem", ".env"],
  "require_confirmation": ["rm -rf", "DROP TABLE", "DELETE FROM"],
  "cost_limits": {
    "per_operation": 10.0,
    "per_hour": 100.0
  }
}
```

## 许可证

MIT License
