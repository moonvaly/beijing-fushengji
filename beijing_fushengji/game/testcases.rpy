testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 8.0

        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit


testcase smoke_intro_to_market:
    click "开始游戏"
    advance until "去货摊看看今天卖什么。"
    click "换个黑市，过一天。"
    advance until screen "map_select"
    assert screen "map_select"
    click "西直门"
    advance until "去货摊看看今天卖什么。"
    click "去银行。"
    advance until "走错了。"
    click "走错了。"
    advance until "去货摊看看今天卖什么。"
    click "去货摊看看今天卖什么。"
    advance until screen "stall_board"
    assert screen "stall_board"
    click "离开货摊"
    advance until "去货摊看看今天卖什么。"
