# ==========================================
# 1. 角色与文字颜色
# ==========================================
define narrator = Character(None, what_color="#3c3d3f")
define t = Character("佟时雨", color="#53617f")
define s = Character("宋艺可", color="#98934b")

# ==========================================
# 2. 图片注册（放 game/images/ 下，靠自动扫描最省事）
#    如果你确认文件都在 images/ 里，这一段可以全删；
#    保留也行，但路径要和实际文件一致。
# ==========================================
image bus = "bus.png"
image daojishi = "daojishi.png"
image schoolzoulang = "schoolzoulang.png"
image tongshiyu = "tongshiyu.png"
image songyike = "songyike.png"
image leaves = "leaves.png"
image schoolyuanjing = "schoolyuanjing.png"
image bg_floor3 = "bg_floor3.png"

# ==========================================
# 3. 立绘位置 transform
# ==========================================
transform left_char:
    zoom 0.5
    xalign 0.05
    yalign 1.0

transform right_char:
    zoom 0.8
    xalign 1.0
    yalign 1.0

transform center_char:
    zoom 0.8
    xalign 0.5
    yalign 1.0

# ==========================================
# 4. 数值 default
# ==========================================
default song_favor = 0
default song_trust = 10

# ==========================================
# 5. 地图状态 default
# ==========================================
default px = 640
default py = 400
default walk_speed = 5

# 房间判定矩形（x1, y1, x2, y2）——图生成后按实际位置改
default room_classroom = (230, 380, 520, 510)  # 第三个房间（中间偏下）
default room_computer  = (230, 560, 520, 680)  # 第四个房间（最下方）

# 墙/障碍矩形列表，角色下一步落在里面就不动
default walls = [
    # (x1, y1, x2, y2),
]

default in_floor3_walk = True
default visited_computer_room = False

# 按键状态（keydown/keyup 记录，供 update_walk 读取）
default key_left = False
default key_right = False
default key_up = False
default key_down = False

# ==========================================
# 6. 移动逻辑
# ==========================================
init python:
    def in_rect(x, y, r):
        return r[0] <= x <= r[2] and r[1] <= y <= r[3]

    def blocked(x, y):
        if x < 40 or x > 1240 or y < 40 or y > 680:
            return True
        for w in store.walls:
            if in_rect(x, y, w):
                return True
        return False

    def update_walk():
        if not store.in_floor3_walk:
            return
        dx = dy = 0
        if store.key_left:  dx -= 1
        if store.key_right: dx += 1
        if store.key_up:    dy -= 1
        if store.key_down:  dy += 1

        if not (dx or dy):
            return

        import math
        l = math.sqrt(dx * dx + dy * dy)
        nx = store.px + int(store.walk_speed * dx / l)
        ny = store.py + int(store.walk_speed * dy / l)

        # 分轴判断，贴墙滑动
        if not blocked(nx, store.py):
            store.px = nx
        if not blocked(store.px, ny):
            store.py = ny

        # 房间判定
        if in_rect(store.px, store.py, store.room_classroom):
            store.in_floor3_walk = False
            renpy.jump("classroom_main")
        elif in_rect(store.px, store.py, store.room_computer):
            store.in_floor3_walk = False
            renpy.jump("computer_room_extra")

# ==========================================
# 7. Screen 定义
# ==========================================
screen status_hud():
    zorder 100
    frame:
        xalign 0.98
        yalign 0.02
        background "#00000080"
        padding (15, 15)
        vbox:
            text "好感: [song_favor]" color "#ffb3b3" size 22
            text "信任: [song_trust]" color "#a8c5ff" size 22

screen floor3_walk():
    add "bg_floor3"
    add "tongshiyu" xpos px ypos py xanchor 0.5 yanchor 0.5 zoom 0.3

    # 按下 / 松开 记录状态（WASD + 方向键）
    key "keydown_K_a"      action SetVariable("key_left", True)
    key "keyup_K_a"        action SetVariable("key_left", False)
    key "keydown_K_LEFT"   action SetVariable("key_left", True)
    key "keyup_K_LEFT"     action SetVariable("key_left", False)

    key "keydown_K_d"      action SetVariable("key_right", True)
    key "keyup_K_d"        action SetVariable("key_right", False)
    key "keydown_K_RIGHT"  action SetVariable("key_right", True)
    key "keyup_K_RIGHT"    action SetVariable("key_right", False)

    key "keydown_K_w"      action SetVariable("key_up", True)
    key "keyup_K_w"        action SetVariable("key_up", False)
    key "keydown_K_UP"     action SetVariable("key_up", True)
    key "keyup_K_UP"       action SetVariable("key_up", False)

    key "keydown_K_s"      action SetVariable("key_down", True)
    key "keyup_K_s"        action SetVariable("key_down", False)
    key "keydown_K_DOWN"   action SetVariable("key_down", True)
    key "keyup_K_DOWN"     action SetVariable("key_down", False)

    timer 0.03 repeat True action Function(update_walk)

       # 兜底点击（字体颜色和大小，位置标在房间正中间）
    textbutton "教室":
        xpos 1000 ypos 220           # 对应第三个房间中心
        xanchor 0.5                 # 让文字居中对齐这个坐标
        yanchor 0.5
        text_color "#6e7ba3"        
        text_hover_color "#ffffff"  # 悬停变白
        text_size 26
        action [SetVariable("in_floor3_walk", False), Jump("classroom_main")]

    textbutton "微机室":
        xpos 1000 ypos 520           # 对应第四个房间中心
        xanchor 0.5
        yanchor 0.5
        text_color "#6e7ba3"       
        text_hover_color "#ffffff"
        text_size 26
        action [SetVariable("in_floor3_walk", False), Jump("computer_room_extra")]

    text "WASD / 方向键 移动" xpos 20 ypos 690 size 18 color "#ffffff"

# ==========================================
# 8. 剧情
# ==========================================
label start:
    show screen status_hud

    # 1. 梦境
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

    show tongshiyu at center_char with dissolve
    "佟时雨拎起书包，透过反光的玻璃看见自己厚厚的齐刘海和黑框眼镜，校服套在瘦削的身体上显得有些空荡。"
    "门缓缓打开，她撑起伞，雨珠噼里啪啦落在伞面上。"
    hide tongshiyu

    # 3. 校园
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
    show tongshiyu at center_char with dissolve
    "那道瘦削的背影停下脚步，回头，眼睛半藏在眼镜和厚厚的刘海后面。宋艺可胳膊上戴着红袖章，拿着DV机，一路小跑到她身边。"
    hide tongshiyu

    show songyike at right_char with dissolve
    s "我是学生会值班的。现在应该是自习课吧。你怎么不上课，跑到教学楼底下来了？"

    show tongshiyu at left_char with dissolve
    "佟时雨没说话。宋艺可觉得今天对方很奇怪。明明是一样的打扮，却给她一种陌生的感觉。"

    s "第一次抓到就算了，我当没看见，你赶紧回教室吧。等会儿景序要是看到了，保准扣我们班分……"
    "佟时雨盯着那边显示屏上几个大大的红字'距离终测还有100天'"

    # 5. 关键选项
    menu:
        "问关于终测的事":
            $ song_favor += 5
            $ song_trust -= 2
            jump branch_ask

        "假装没事回教室":
            $ song_favor -= 5
            $ song_trust += 5
            jump branch_leave

# ==========================================
# 大分支 1：问关于终测的事
# ==========================================
label branch_ask:
    t "那边显示屏上的话是什么意思？"
    s "终测呀。就是我们在那一天通过'终极测试'，凭借测试分数报考大学，选择以后的专业。"
    s "现在距离那一天还有100天。今天还要办动员大会呢。"
    t "(终测……我记得分为精神测试和体能测试。)"

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
# 公共结尾（数值判定）
# ==========================================
label ending_scene:
    hide songyike
    scene schoolzoulang with fade
    "走在教学楼内，栏杆把校园一分为二。"
    "栏杆外是大雨欲来的天空，凭白昼的时辰维持着昏暗的光；栏杆内是熄灯的走廊，切割光影后借一点外界的光，使其不至于像傍晚。"
    "她感觉自己好像做了一个很长的梦。"
    t "（自己的意识与身体保持弱连接太久了……）"

    if song_trust >= 12:
        "转过拐角，一滴颜料从天花板上忽地坠落。佟时雨感觉口袋里多了一样东西。"
        "……是刚才擦肩而过时，宋艺可偷偷塞给她的一张小纸条。"
        t "（上面写着：『今晚小心。』）"
    else:
        "佟时雨回头看了一眼，宋艺可正站在原地，用审视的目光盯着她的背影。"
        t "（她似乎对我起疑心了……）"

    # 进入三楼地图
    jump floor3_map

# ==========================================
# 9. 地图 label
# ==========================================
label floor3_map:
    $ px = 640
    $ py = 400
    $ in_floor3_walk = True
    $ key_left = False
    $ key_right = False
    $ key_up = False
    $ key_down = False
    call screen floor3_walk
    return

label classroom_main:
    scene bg_classroom
    "（教室主线剧情占位）"
    jump floor3_map

label computer_room_extra:
    scene bg_computer_room
    if not visited_computer_room:
        $ visited_computer_room = True
        "（微机室额外剧情占位）"
    else:
        "这里已经看过了。"
    jump floor3_map