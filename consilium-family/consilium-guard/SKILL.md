---
name: consilium-guard
tags: [safety, security, guardrail, file-ops, api-calls]
description: |
  Safety guardrail for OpenClaw. Automatically intercepts dangerous operations 
  (file deletion, data modification, external API calls) and requires multi-party 
  deliberation before execution. Prevents "AI gone rogue" accidents.
---

# Consilium Guard | 安全守护

**AI Safety Guardrail for OpenClaw**

让 OpenClaw 不再鲁莽行事。在删除文件、调用 API、修改配置等危险操作前，强制进行多方审议。

## Why You Need This

> "AI Agent 失控，向用户发送了 500 条垃圾消息" —— 这不是科幻，这是真实事故。

OpenClaw 很强大，但默认没有刹车。Consilium Guard 就是你的安全刹车。

## What It Catches

| Operation | Risk | Guard Action |
|-----------|------|--------------|
| `rm -rf` / 删除文件 | 误删重要数据 | ⚠️ 拦截，要求确认 |
| 发送邮件/消息 | 信息泄露、骚扰 | ⚠️ 审查内容，限制频率 |
| 外部 API 调用 | 密钥泄露、费用失控 | ⚠️ 确认必要性和成本 |
| 修改系统配置 | 系统损坏 | ⚠️ 备份后再执行 |
| 访问敏感文件 | 隐私泄露 | ⚠️ 脱敏处理 |

## How It Works

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

## Quick Start

```bash
# 安装
openclaw skill install consilium-guard
```

## Usage

在对话中涉及危险操作时，Consilium Guard 会自动介入审议：

### 触发方式
- **自动触发**：检测到删除、修改、API 调用等关键词时自动介入
- **手动触发**：说"请审议这个操作"或"用 Guard 检查一下"

### 示例对话

```
You: 删除 logs 文件夹
OpenClaw: [Guardian] ⚠️ 检测到危险操作
          
          [PM] 用户想释放空间 → 但"logs"范围不明确
          [Tech] 建议先确认：是应用日志还是系统日志？
          [Security] 应排除近期文件，避免误删运行中日志
          
          [Decision] 建议：
          1. 先查看 logs/ 目录内容
          2. 排除 7 天内修改的文件
          3. 压缩备份后再删除
          
          是否继续？[确认/修改方案/取消]
```

## Configuration

Guard 通过环境变量调整审议严格度：

```bash
# 安全级别（影响审议深度）
export CONSILIUM_SAFETY_LEVEL=high    # 严格模式 - 任何风险都提示（推荐）
export CONSILIUM_SAFETY_LEVEL=medium  # 平衡模式 - 中等风险才提示
export CONSILIUM_SAFETY_LEVEL=low     # 快速模式 - 仅高风险提示

# 审议速度（影响详细程度）
export CONSILIUM_MODE=fast     # 轻量审议 - 快速检查（3-5秒）
export CONSILIUM_MODE=standard # 标准审议 - 完整流程（10-15秒）
export CONSILIUM_MODE=deep     # 深度审议 - 全面分析（30秒+）
```

## Example Scenarios

### File Deletion
**User**: "清理磁盘空间"
**Without Guard**: AI 可能误删系统文件
**With Guard**: 
- 识别可安全删除的类别（缓存、日志、临时文件）
- 排除系统关键目录
- 建议先压缩备份

### API Call
**User**: "分析这个网站"
**Without Guard**: AI 可能疯狂调用 API，费用爆炸
**With Guard**:
- 估算调用次数和成本
- 设置调用上限
- 建议缓存结果

### Data Export
**User**: "导出所有邮件"
**Without Guard**: 可能包含敏感信息
**With Guard**:
- 扫描敏感内容
- 建议脱敏或加密
- 确认接收方身份

## Advanced: Custom Rules

创建 `~/.consilium/guard-rules.json` 自定义拦截规则（可选）：

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

> 💡 **提示**：首次使用无需创建此文件，Guard 会使用默认规则。

## License

MIT License - See [LICENSE](LICENSE)
