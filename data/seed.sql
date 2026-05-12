-- Compass cold-start seed data
-- Run after `compass init` via `compass seed` or directly: sqlite3 crm.db < data/seed.sql
-- Uses INSERT OR IGNORE so it is idempotent and safe to re-run.
-- All timestamps are fixed at 2026-05-12T00:00:00Z for reproducibility.

PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO target (id, name, kind, tier, status, notes_path, created_at) VALUES
  ('target_bdy',  '字节跳动',     'job',       'dream',  'active', NULL, '2026-05-12T00:00:00Z'),
  ('target_hf',   'Hugging Face', 'job',       'strong', 'active', NULL, '2026-05-12T00:00:00Z'),
  ('target_blog', 'My Blog',      'media',     'try',    'active', NULL, '2026-05-12T00:00:00Z'),
  ('target_fwd',  '朋友们',        'community', 'try',    'active', NULL, '2026-05-12T00:00:00Z');

INSERT OR IGNORE INTO lane (id, target_id, kind, title, stage, deadline, asset_id, status, created_at, closed_at) VALUES
  ('lane_bdy_l7',  'target_bdy',  'job_app',  'L7 Staff Engineer (Go)', 'interview', NULL, NULL, 'active', '2026-05-12T00:00:00Z', NULL),
  ('lane_bdy_l6',  'target_bdy',  'job_app',  'L6 Senior Engineer (Go)', 'applied',   NULL, NULL, 'active', '2026-05-12T00:00:00Z', NULL),
  ('lane_hf_mle',  'target_hf',   'job_app',  'ML Engineer',             'open',      NULL, NULL, 'active', '2026-05-12T00:00:00Z', NULL),
  ('lane_blog',    'target_blog', 'content',  'Static Analysis Series',  'closed',    NULL, NULL, 'active', '2026-05-12T00:00:00Z', NULL),
  ('lane_fwd',     'target_fwd',  'outreach', 'Coffee Chats Network',     'open',      NULL, NULL, 'active', '2026-05-12T00:00:00Z', NULL);

INSERT OR IGNORE INTO touchpoint (id, lane_id, kind, summary, insights, next_step, happened_at) VALUES
  ('tp1',  'lane_bdy_l7',  'message',  '猎头 Alice 联系，推荐 L7 Staff Engineer 职位，要求 5 年以上 Go 经验。',                                  '字节跳动后端使用 Go，技术栈匹配。',                       '回复猎头，确认感兴趣，约定电话时间。',       '2026-04-20T10:00:00Z'),
  ('tp2',  'lane_bdy_l7',  'call',     '与猎头 Alice 通电话，了解团队方向：字节跳动云基础设施部门，做大规模分布式存储。',                        '团队规模约 50 人，用 Go + etcd，技术挑战大。',            '周一发送简历和 GitHub 链接。',              '2026-04-22T15:00:00Z'),
  ('tp3',  'lane_bdy_l7',  'applied',  '通过猎头正式提交 L7 申请，附简历 + GitHub + LinkedIn。',                                                '简历突出了 Go 性能和分布式系统经验。',                  '等待 hr 联系，约第一轮技术面。',            '2026-04-24T09:00:00Z'),
  ('tp4',  'lane_bdy_l7',  'call',     '第一轮技术面：算法（LRU Cache）+ 系统设计（设计一个短链服务）。用 Go 写了 LRU。',                     '算法题较简单；系统设计需要补充 CAP 理论细节。',         '复盘系统设计，准备二面。',                  '2026-04-28T14:00:00Z'),
  ('tp5',  'lane_bdy_l7',  'call',     '第二轮技术面：深入项目经历，问了 etcd 源码、raft 协议、内存管理、GC 调优。',                          '对 Go 底层了解还需加强，特别是 GC 和内存分配细节。',   '阅读《Go 源码看得见》相关章节，准备三面。', '2026-05-05T10:00:00Z'),
  ('tp6',  'lane_bdy_l7',  'message',  '收到 HR 消息，三面（HR + 交叉面）定在周五下午。',                                                      '',                                                      '准备自我介绍和职业价值观回答。',            '2026-05-08T11:00:00Z'),
  ('tp7',  'lane_bdy_l6',  'applied',  '同步投递 L6 Senior 职位（另一个部门），已提交简历。',                                                  'L6 和 L7 可以并行，保留选项。',                          '等待 L6 hr 联系。',                          '2026-04-25T09:00:00Z'),
  ('tp8',  'lane_hf_mle',  'message',  '浏览 Hugging Face 招聘页面，ML Engineer 职位要求：PyTorch 深度优化、LLM inference、分布式训练。',     '需要补足 PyTorch 和 LLM 相关经验。',                     '下周开始学习 PyTorch 官方教程。',           '2026-05-01T20:00:00Z'),
  ('tp9',  'lane_blog',    'post',     '发布技术博客文章：《看得见的 Go 内存分配》，介绍了 tcmalloc 和 Go 内存分配器原理。',                   '文章获得较好反馈，有读者问到与 Rust 分配的对比。',       '续写：《看得见的 GC》— Go GC 源码解读。',   '2026-04-15T18:00:00Z'),
  ('tp10', 'lane_fwd',     'meet',     '和大学同学李明喝咖啡，他现在在阿里云做存储。聊了职业方向和市场行情。',                                 '阿里云 P8+ 在看外部机会，市场比想象中冷。',              '保持联系，有机会互相推荐。',                '2026-05-03T16:00:00Z');
