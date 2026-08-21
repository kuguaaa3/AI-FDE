# AI FDE｜企业业务实施智能体

> 让企业教会 AI 工作，而不是让企业先学会怎么用 AI。

本仓库为 2026 Super Agent 开放赛道报名原型与 P0 技术验证材料。

## 核心命题

AI FDE 不重新发明一个通用 Agent 平台，而是解决 AI 落地的最后一公里：

**Teach / Record → Semantic Trace → Business Skill → User Correction → New-case Execution → Independent Verification**

系统首先适应企业现有流程。AI 推断与优化建议不会自动覆盖企业规则；用户确认与修改会进入版本化 Business Skill。

## P0 验证结果

当前结论：**CORE ENGINE PASS / HUMAN TEACH NOT YET VERIFIED**

- AC-01～AC-07：7/7 PASS
- 捕获 22 个运行事件，其中 16 个 trusted DOM 事件
- Business Skill V1 → 用户修正 → V2 版本链通过
- Day-2 新数据执行：净销售 15000
- 独立只读 System-of-Record 接口确认：值精确一致，且仅 1 条记录
- 故障轨：UI 显示成功但后端未落库时返回 `NOT_VERIFIED` 并 HALT
- OpenAdapt 1.13.1：录制、编译、认证完成；clean replay 因独立 verifier 不可达而 Fail Closed，因此标记 PARTIAL

未验证：真人 Teach、真实企业系统、Windows/跨应用生产链、生产级稳定性。

## 快速复现 P0

```bash
cd demo
python -m pip install -r requirements.txt
python run_spike.py
```

完整结果与证据见 `evidence/`。

## 目录

- `docs/`：报名文案、项目计划书、技术架构、合规说明
- `demo/`：最小可运行 P0 Spike
- `fixtures/`：Day-1 / Day-2 合成业务数据与用户修正规则
- `schemas/`：Business Skill / Execution Request Schema
- `evidence/`：Semantic Trace、Skill V1/V2、Day-2 执行、独立验真、故障轨与 Manifest

## 核心边界

1. Adapt to the Business, not Reform the Business.
2. AI 推断不能自动升级为企业事实。
3. 用户可以修改规则、人工 Gate 与验收标准，并形成新 Skill 版本。
4. 稳定步骤优先确定性执行，AI 主要用于理解、异常和模糊判断。
5. Agent 自报完成不算完成，真实业务状态独立验真后才算完成。

## 验证包哈希

Walker 原始 P0 Return ZIP SHA-256：

`edb8ef793b4ec9580049a6d208655f505d285626bf8bb4cbe5b9caec33ab2d86`
