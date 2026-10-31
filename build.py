# Regenerates index.html from data.json. Usage: python3 build.py
import json,html,datetime,collections
D=json.load(open('data.json'));P=D['posts'];pr=D['profile']
BJ=datetime.timezone(datetime.timedelta(hours=8))
def bj(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(BJ)
THEMES=[('🛠 自家产品持续迭代',['Mole','MiaoYan','Kaku','Waza','Pake','Kami','license','图标']),
('🧭 多端客户端技术选型',['技术选型','Windows 软件','技术栈','书接','连载']),
('🤖 AI 编程工具实战',['Claude','Codex','ChatGPT','Gemini','Grok','opus','Agent','AI']),
('🌿 个人观点与生活',[''])]
def theme(t):
  for n,ks in THEMES:
    if any(k and k.lower() in t.lower() for k in ks):return n
  return THEMES[-1][0]
for p in P:p['theme']=theme(p['text'])
esc=lambda s:html.escape(s)
def snip(t,n=120):
  t=' '.join(w for w in t.split() if not w.startswith('https://t.co'));return esc(t[:n]+('…' if len(t)>n else '')) or '（图片/链接帖）'
def card(p):return f'<a class="post" href="{p["url"]}" target="_blank" rel="noopener"><div class="meta">{bj(p["created_at"]):%m-%d %H:%M}</div><p>{snip(p["text"])}</p><div class="stats">❤️ {p["likes"]:,} · 🔖 {p["bookmarks"]:,} · 👁 {p["impressions"]:,}</div></a>'
first,last=bj(P[-1]['created_at']),bj(P[0]['created_at'])
tl=sum(p['likes'] for p in P);tb=sum(p['bookmarks'] for p in P);ti=sum(p['impressions'] for p in P)
th=''
for n,_ in THEMES:
  ps=sorted([p for p in P if p['theme']==n],key=lambda p:-(p['likes']+p['bookmarks']))
  th+=f'<section class="theme"><h3>{n} <span class="pill">{len(ps)} 条</span></h3><div class="grid">{"".join(card(p) for p in ps[:4])}</div></section>'
top=sorted(P,key=lambda p:-(p['likes']+p['bookmarks']))[:8]
topH=''.join(f'<li><a href="{p["url"]}" target="_blank" rel="noopener">{snip(p["text"],70)}</a><span>❤️ {p["likes"]:,} · 🔖 {p["bookmarks"]:,}</span></li>' for p in top)
day=collections.OrderedDict()
d0=first.date()
while d0<=last.date():day[d0]=[0,0];d0+=datetime.timedelta(days=1)
for p in P:
  k=bj(p['created_at']).date();day[k][0]+=1;day[k][1]+=p['likes']+p['bookmarks']
mx=max(v[1] for v in day.values()) or 1;W=760;H=200;bw=W/len(day)
bars=''.join(f'<rect x="{i*bw+1:.1f}" y="{H-20-(v[1]/mx)*(H-40):.1f}" width="{bw-2:.1f}" height="{(v[1]/mx)*(H-40):.1f}" rx="2"><title>{k:%m-%d}：{v[0]} 条，互动 {v[1]:,}</title></rect>'+(f'<text x="{i*bw+bw/2:.1f}" y="{H-4}">{k:%m-%d}</text>' if i%5==0 else '') for i,(k,v) in enumerate(day.items()))
chart=f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="每日互动">{bars}</svg>'
heat=''.join(f'<div class="cell" style="--a:{min(v[0],6)/6:.2f}" title="{k:%m-%d}：{v[0]} 条"></div>' for k,v in day.items())
INS=[('一个产品长期做，并且公开做','MiaoYan 做了 6 年才上 iPhone/iPad；Mole CLI 仅 10 月就发了 18 个版本；Kami 1.20 补上图表校验、产品站配色与中韩移动端排版——每个里程碑都发推讲清楚更新了什么。','https://x.com/HiTw93/status/2116163296437104926'),
('用“笨功夫”建立壁垒','手工自测 800 款 Mac 软件、372 款 Windows 软件的卸载，逐一重发 400+ 封许可证邮件——这些细节 AI 堆不出来。','https://x.com/HiTw93/status/2106964278507118794'),
('开源引流，付费变现','Mole CLI 开源收获 7.28 万 Star，图形版（Mac/Windows $15.20）与 MiaoYan 移动端收费，同时接受 GitHub Sponsors。','https://x.com/HiTw93/status/2110371329354698962'),
('追着 AI 找新需求','给 Mole 加 “AI 清理与维护”：清理 Claude Code、Codex 的缓存、旧会话与 worktree，并提供 agent 可调用的 skill。','https://x.com/HiTw93/status/2105509778307080627'),
('干货长文是最好的获客','多端技术选型三连载、Grok Bot 提示词、Android 去广告教程，以及 10/28 把自己的 AI Coding 经验整理成可复用的最佳实践规则（一天内 700+ 收藏）；次日又发英文版《20 条 AI 编程规则》，一天收获 900+ 收藏、4 万浏览，同一份干货中英双发，触达海外读者。收藏量动辄数百上千，远超产品宣传帖。','https://x.com/HiTw93/status/2115805352520282623'),
('守住“活人感”与长期主义','不接商单以免伤害未来用户、警惕 AI 式回复、持续 6 年的潮流周刊——真实的个人品牌在 AI 时代更值钱。','https://x.com/HiTw93/status/2114230677604557136')]
insH=''.join(f'<div class="ins"><b>{i+1:02d}</b><h4>{a}</h4><p>{b}</p><a href="{c}" target="_blank" rel="noopener">相关推文 →</a></div>' for i,(a,b,c) in enumerate(INS))
now=datetime.datetime.now(BJ)
CSS='''
:root{--bg:#f7f7f5;--fg:#16181c;--mut:#6b7280;--card:#fff;--bd:#e5e7eb;--ac:#6d5efc;--ac2:#14b8a6}
@media(prefers-color-scheme:dark){:root{--bg:#0e1015;--fg:#e8eaed;--mut:#9aa0aa;--card:#171a21;--bd:#262a33;--ac:#8b80ff;--ac2:#2dd4bf}}
*{box-sizing:border-box}body{margin:0;font:16px/1.7 -apple-system,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--fg)}
.wrap{max-width:1040px;margin:auto;padding:24px 20px 60px}a{color:inherit;text-decoration:none}
.hero{padding:48px 32px;border-radius:24px;background:linear-gradient(135deg,var(--ac),var(--ac2));color:#fff;margin-bottom:36px}
.hero h1{margin:0 0 6px;font-size:clamp(28px,5vw,44px)}.hero p{margin:0;opacity:.9}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-top:26px}
.kpi{background:rgba(255,255,255,.16);border-radius:14px;padding:12px 14px}.kpi b{display:block;font-size:24px}.kpi span{font-size:13px;opacity:.85}
h2{font-size:24px;margin:44px 0 16px}h2 small{font-size:14px;color:var(--mut);font-weight:400;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.post,.ins{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:16px;display:flex;flex-direction:column;transition:.2s}
.post:hover{transform:translateY(-3px);border-color:var(--ac)}.post p{flex:1;margin:6px 0;font-size:14.5px}
.meta,.stats{font-size:12.5px;color:var(--mut)}.pill{font-size:12px;background:var(--ac);color:#fff;border-radius:99px;padding:2px 10px;vertical-align:middle}
.theme h3{margin:28px 0 12px}
ol.top{padding:0;list-style:none;counter-reset:n}ol.top li{counter-increment:n;display:flex;gap:12px;align-items:baseline;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--bd)}
ol.top li:before{content:counter(n);font-weight:700;color:var(--ac);min-width:22px}ol.top li a{flex:1}ol.top li a:hover{color:var(--ac)}ol.top span{white-space:nowrap;font-size:13px;color:var(--mut)}
.box{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:18px}
svg{width:100%;height:auto}svg rect{fill:var(--ac)}svg rect:hover{fill:var(--ac2)}svg text{font-size:10px;fill:var(--mut)}
.heat{display:grid;grid-template-columns:repeat(auto-fill,minmax(22px,1fr));gap:5px}.cell{aspect-ratio:1;border-radius:5px;background:color-mix(in srgb,var(--ac2) calc(var(--a)*100%),var(--bd))}
.ins b{color:var(--ac);font-size:22px}.ins h4{margin:4px 0}.ins p{flex:1;font-size:14.5px;color:var(--mut);margin:4px 0 10px}.ins a{color:var(--ac);font-size:14px}
footer{margin-top:50px;font-size:13px;color:var(--mut);text-align:center}
@media(max-width:600px){.hero{padding:32px 20px}ol.top li{flex-wrap:wrap}}
'''
out=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tw93 动态洞察 · 独立开发者观察</title><meta name="description" content="基于 @HiTw93 公开推文的总结与分析"><style>{CSS}</style></head><body><div class="wrap">
<header class="hero"><h1>Tw93 动态洞察</h1><p>{esc(pr["description"])} 的作者 · 基于 @{pr["username"]} 公开原创推文的非官方分析</p>
<div class="kpis"><div class="kpi"><b>{pr["followers"]:,}</b><span>关注者</span></div><div class="kpi"><b>{len(P)}</b><span>本期原创帖</span></div><div class="kpi"><b>{tl:,}</b><span>累计点赞</span></div><div class="kpi"><b>{tb:,}</b><span>累计收藏</span></div><div class="kpi"><b>{ti/1e4:,.0f} 万</b><span>累计浏览</span></div></div>
<p style="margin-top:16px;font-size:14px">覆盖 {first:%Y-%m-%d} – {last:%Y-%m-%d}（北京时间），不含转推与回复</p></header>
<h2>他最近在说什么<small>按主题自动归类，每类展示互动最高的 4 条</small></h2>{th}
<h2>互动最高的帖子<small>点赞 + 收藏</small></h2><div class="box"><ol class="top">{topH}</ol></div>
<h2>每日互动<small>悬停查看当天条数与互动量</small></h2><div class="box">{chart}</div>
<h2>发帖节奏<small>每格一天，颜色越深发得越多</small></h2><div class="box"><div class="heat">{heat}</div></div>
<h2>对独立开发者的启示</h2><div class="grid">{insH}</div>
<footer>最后更新：{now:%Y-%m-%d %H:%M}（北京时间） · 数据来自 X 公开推文 · 非 X 官方页面 · <a href="https://x.com/HiTw93" target="_blank" rel="noopener">@HiTw93</a></footer>
</div></body></html>'''
open('index.html','w').write(out);print('ok',len(P))
