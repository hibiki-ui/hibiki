"""macUI Testing Framework

分层测试策略:
- unit/: 单元测试 (80%) - 纯逻辑，Mock PyObjC
- integration/: 集成测试 (15%) - 真实 PyObjC 交互  
- snapshots/: 快照测试 (5%) - 结构回归检测
"""