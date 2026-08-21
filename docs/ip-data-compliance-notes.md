# 原创 / IP / 数据合规与材料口径

## 原创与知识产权
项目的产品定义、Business Skill 数据契约、用户治理逻辑、Demonstration-to-Skill Compiler、Change/Version/Acceptance 机制以及 P0 集成实现由团队自主设计与开发。

底层可能复用 OpenAdapt、Playwright、DeepSeek Harness、Codex、Claude Code、Coze 等第三方/开源能力。所有第三方能力按各自许可证与服务条款使用，并在材料中明确不把第三方底层能力描述为自研成果。

## 数据合规
当前 P0 完全使用本地合成经营数据、本地网页 fixture 与本地 backend，不包含真实企业数据或个人敏感信息。

未来产品默认采用：主动 Teach 授权、最小权限、范围限定、敏感字段脱敏/排除、本地/私有部署优先、高风险操作人工 Gate、审计留痕、结果独立验真、Fail Closed。

## 报名口径边界
可以写：CORE ENGINE PASS；浏览器本地合成场景 7/7 PASS；V1→V2；Day-2 15000；独立 verifier；故障轨 Fail Closed。

不能写：真人 Teach 已验证；OpenAdapt 已完整集成；真实企业已部署；生产级稳定；一次示范学会所有复杂流程；完全无需人工；AI 自动改革企业。
