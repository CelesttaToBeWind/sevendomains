# --- 定义角色和文字颜色 ---
define narrator = Character(None, what_color="#3c3d3f") 
define t = Character("佟时雨", color="#53617f")
define s = Character("宋艺可", color="#98934b")

# --- 注册你的图片 ---
image bus = "bus.png"
image daojishi = "daojishi.png"
image schoolzoulang = "schoolzoulang.png"
image tongshiyu = "tongshiyu.png"
image songyike = "songyike.png"
image leaves = "leaves.png"
image schoolyuanjing = "schoolyuanjing.png"

# 定义人物立绘的位置和大小
transform left_char:
    zoom 0.5
    xalign 0.05
    yalign 1.0

transform right_char:
    zoom 0.8
    xalign 1.0
    yalign 1.0

transform center_char:
    zoom 0.2
    xalign 0.5
    yalign 1.0

# 故事开始
label start:
    # 1. 梦境部分
    scene black with fade
    "最先感觉到的是阳光的呼吸，轻轻拍在脸上。"
    "风带着热度送来几缕野花的清香。于是她掀开蒙蔽的黑色幕布。"
    "刹那，金色直泻而下，从脚尖爬上小腿，裙摆，然后是脸颊。泛着金光的蝴蝶自鼻尖振翅起飞，跃向青蓝色的天空。"
    "她不由自主地向前奔去，踏过花丛，踏过野草，阳光下近乎透明的翅膀闪动，共舞的花瓣似乎也被晕染上了柔光。"
    "没人知道那是黄昏还是黎明，夕阳和初日的界限模糊不清。可生命的颂歌却随风流转，奔腾不息。"
    "忽地，强烈的扭曲感袭来，仿佛灵魂正逃出这梦境一般的画面。混沌、恶心、头疼……"

    # 2. 公交车醒来
    scene bus with vpunch 
    "她终于睁开眼，看到的是玻璃外灰蒙蒙的天空、暗色的向后闪过的街道。"
    
    t "（脑子麻麻的。我居然还活着吗……）"
    "我正在念高三。应该是在三年前，我仿佛突然失去了思考的能力，只是像摄像头一般地活着。"
    "我记得这三年来的事，但我在这段日子里只是按部就班。对于这些年发生的事，我几乎没有什么思考和感触。"
    t "就像……有人给我设置好了代码，我只是遵循代码在执行程序。"
    "公交车转了一个弯，进入了更宽敞的街道，随后缓缓减速。车内响起语音播报：'七区二十中到了。开门请当心。'"

    show tongshiyu at center with dissolve 
    "佟时雨拎起书包，透过反光的玻璃看见自己厚厚的齐刘海和黑框眼镜，校服套在瘦削的身体上显得有些空荡。"
    "门缓缓打开，她撑起伞，雨珠噼里啪啦落在伞面上。"
    hide tongshiyu
    
    # 3. 倒计时显示屏
    scene schoolyuanjing with fade
    "七区二十中校园面积很大，环境优美。教学质量虽然比不上七区一中，在整个第七区也是保三争二。"
    "光隐入云层，取而代之的是蒙蒙的灰调。漫步在校园内，学生们大都身着统一的校服，行色匆匆。"

    scene leaves with fade
    "一片枯叶被框在灰白色的空镜里。快门按下的一瞬间，枯叶被一只脚踩过，'咔擦'一声，叶身爬上几丝裂缝。"

    scene schoolyuanjing with fade    
    show songyike at right_char with dissolve
    "宋艺可收起DV机，目光落在不远处走过去的人身上。"
    "她认出那是她们班的一个小透明女生，成绩总是垫底，平时也沉默寡言，几乎不和人说话。"
    "也许是她很听话不惹事，老师批评人也批评不到她身上，谈成绩时却也不怎么谈她。久而久之，她的存在感低到像被全班孤立的状态。"
    s "佟时雨?"

    scene daojishi with fade
    hide songyike
    show tongshiyu at center with dissolve 

    "那道瘦削的背影停下脚步，回头，眼睛半藏在眼镜和厚厚的刘海后面。宋艺可胳膊上戴着红袖章，拿着DV机，一路小跑到她身边。"
    hide tongshiyu

    show songyike at right_char with dissolve
    s "我是学生会值班的。现在应该是自习课吧。你怎么不上课，跑到教学楼底下来了？"

    show tongshiyu at left_char with dissolve 
    "佟时雨没说话。宋艺可觉得今天对方很奇怪。明明是一样的打扮，却给她一种陌生的感觉。"

    s "第一次抓到就算了，我当没看见，你赶紧回教室吧。等会儿景序要是看到了，保准扣我们班分……"
    "佟时雨盯着那边显示屏上几个大大的红字'距离终测还有100天'"
    
    # 5. 关键选项（多分支）
    menu:
        "问关于终测的事":
            jump branch_ask 
        "假装没事回教室":
            jump branch_leave 


# ==========================================
# 大分支 1：问关于终测的事
# ==========================================
label branch_ask:
    t "那边显示屏上的话是什么意思？"
    s "终测呀。就是我们在那一天通过'终极测试'，凭借测试分数报考大学，选择以后的专业。"
    s "现在距离那一天还有100天。今天还要办动员大会呢。"
    t "(终测……我记得分为精神测试和体能测试。)"
    
    # 小分支
    menu:
        "询问精神测试": 
            jump small_test_spirita
        "询问体能测试":
            jump small_test_physicala
        "不问了，回教室":
            jump branch_leavea

label small_test_spirita:
    t "精神测试是什么？"
    s "测试{color=#5dbcd2}精神体{/color}的强度。你今天不舒服吗？为什么问这个？"
    "佟时雨若有所思。" 
    jump ending_scene1 

label small_test_physicala:
    t "体能测试是什么？"
    s "就是跑步、力量那些呀。下周就要模拟考了。你连这都忘了吗？"
    "宋艺可震惊地看着她。"
    jump ending_scene1 

label branch_leavea:
    jump ending_scene1

label ending_scene1:
    "佟时雨轻飘飘地带过，幽灵一般朝教学楼走去。"
    t "没什么。抱歉给你带来麻烦了。"
    s "真是奇怪的人……"
    jump ending_scene


# ==========================================
# 大分支 2：假装没事回教室
# ==========================================
label branch_leave:
    t "哦，知道了。"
    "佟时雨轻飘飘地带过，幽灵一般朝教学楼走去。"
    "(终测……我记得分为精神测试和体能测试。可是……)"
    "（嘶。头疼。大概是记忆刚回来没多久，检索起具体细节有些困难……）"

    # 小分支
    menu:
        "回想精神测试": 
            jump small_test_spiritb
        "回想体能测试":
            jump small_test_physicalb
        "不想了，回教室":
            jump ending_scene

label small_test_spiritb:
    t "精神测试……我记得是测试{color=#5dbcd2}精神体{/color}的强度。"
    "……" 
    jump ending_scene2 

label small_test_physicalb:
    t "体能测试……我记得是测试肉体的力量、格斗技巧和健康程度？"
    jump ending_scene2 

label ending_scene2:
    "不知不觉中，佟时雨来到了教学楼。"
    jump ending_scene


# ==========================================
# 公共结尾
# ==========================================
label ending_scene:
    hide songyike
    scene schoolzoulang with fade
    "走在教学楼内，栏杆把校园一分为二。"
    "栏杆外是大雨欲来的天空，凭白昼的时辰维持着昏暗的光；栏杆内是熄灯的走廊，切割光影后借一点外界的光，使其不至于像傍晚。"
    "她感觉自己好像做了一个很长的梦。"
    t "（自己的意识与身体保持弱连接太久了……）"
    return