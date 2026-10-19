"""
The fixed 1024-entry emoji table that emojihash indexes into.

Built from every code point that Unicode 13.0 marks Emoji_Presentation=Yes and not
Emoji_Component (which excludes regional indicators, skin-tone modifiers, and hair
components), in code point order, minus 89 near-duplicates that are hard to tell apart at
small sizes: the 24 clock faces, 7 moon phases, 12 zodiac signs, 10 squared CJK
ideographs, and 36 others such as oncoming-vehicle and banknote variants. Each entry is one
code point with default emoji presentation, so it renders as one glyph without a variation
selector or ZWJ sequence.

The order is part of the output contract: reordering, adding, or removing entries changes
the emoji every input maps to.
"""

EMOJI: tuple[str, ...] = tuple(
    "⌚⌛⏩⏪⏰⏳☔☕♿⚓⚡⚪⚫⚽⚾⛄⛅⛎⛔⛪⛲⛳⛵⛺⛽✅✊✋✨❌❎❓"
    "❔❕❗➕➖➗➰➿⬛⬜⭐⭕🀄🃏🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🈁🉐🉑🌀🌁🌂🌃"
    "🌄🌅🌆🌇🌈🌉🌊🌋🌌🌍🌎🌏🌐🌕🌙🌚🌛🌜🌝🌞🌟🌠🌭🌮🌯🌰🌱🌲🌳🌴🌵🌷"
    "🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗"
    "🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷"
    "🍸🍹🍺🍻🍼🍾🍿🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎠🎡🎢🎣🎤"
    "🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄"
    "🏅🏆🏇🏈🏉🏊🏏🏐🏑🏒🏓🏠🏡🏢🏣🏥🏦🏧🏨🏩🏪🏫🏬🏭🏮🏯🏰🏴🏸🏹🏺🐀"
    "🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠"
    "🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾👀👂"
    "👃👄👅👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢"
    "👣👤👥👦👧👨👩👪👫👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄"
    "💅💆💇💈💉💊💋💌💍💎💐💑💒💓💔💕💖💗💘💙💚💛💜💝💞💟💠💡💢💣💤💥"
    "💦💧💨💩💪💫💬💭💮💯💰💱💲💳💵💸💹💺💻💼💽💾💿📀📁📃📄📅📆📇📈📉"
    "📊📋📌📍📎📏📐📑📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩📫📮📯"
    "📰📱📲📳📵📶📷📸📹📺📻📼📿🔀🔁🔄🔆🔇🔊🔋🔌🔍🔎🔑🔒🔓🔔🔕🔖🔗🔘🔙"
    "🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮🔯🔰🔱🔲🔳🔴🔵🔶🔷🔺🔻"
    "🔼🔽🕋🕌🕍🕎🕺🖕🖖🖤🗻🗼🗽🗾🗿😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐"
    "😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧😨😩😪😫😬😭😮😯😰"
    "😱😲😳😴😵😶😷😸😹😺😻😼😽😾😿🙀🙁🙂🙃🙄🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏🚀"
    "🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚌🚎🚏🚐🚑🚒🚓🚕🚗🚙🚚🚛🚜🚝🚟🚠🚡🚢🚣🚤🚥🚦"
    "🚧🚨🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚶🚷🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛌🛐🛑"
    "🛒🛕🛖🛗🛫🛬🛴🛵🛶🛷🛸🛹🛺🛻🛼🟠🟡🟢🟣🟤🟥🟦🟧🟨🟩🟪🟫🤌🤍🤎🤏🤐"
    "🤑🤒🤓🤔🤕🤖🤗🤘🤙🤚🤛🤜🤝🤞🤟🤠🤡🤢🤣🤤🤥🤦🤧🤨🤩🤪🤫🤬🤭🤮🤯🤰"
    "🤱🤲🤳🤴🤵🤶🤷🤸🤹🤺🤼🤽🤾🤿🥀🥁🥂🥃🥄🥅🥇🥈🥉🥊🥋🥌🥍🥎🥏🥐🥑🥒"
    "🥓🥔🥕🥖🥗🥘🥙🥚🥛🥜🥝🥞🥟🥠🥡🥢🥣🥤🥥🥦🥧🥨🥩🥪🥫🥬🥭🥮🥯🥰🥱🥲"
    "🥳🥴🥵🥶🥷🥸🥺🥻🥼🥽🥾🥿🦀🦁🦂🦃🦄🦅🦆🦇🦈🦉🦊🦋🦌🦍🦎🦏🦐🦑🦒🦓"
    "🦔🦕🦖🦗🦘🦙🦚🦛🦜🦝🦞🦟🦠🦡🦢🦣🦤🦥🦦🦧🦨🦩🦪🦫🦬🦭🦮🦯🦴🦵🦶🦷"
    "🦸🦹🦺🦻🦼🦽🦾🦿🧀🧁🧂🧃🧄🧅🧆🧇🧈🧉🧊🧋🧍🧎🧏🧐🧑🧒🧓🧔🧕🧖🧗🧘"
    "🧙🧚🧛🧜🧝🧞🧟🧠🧡🧢🧣🧤🧥🧦🧧🧨🧩🧪🧫🧬🧭🧮🧯🧰🧱🧲🧳🧴🧵🧶🧷🧸"
    "🧹🧺🧻🧼🧽🧾🧿🩰🩱🩲🩳🩴🩸🩹🩺🪀🪁🪂🪃🪄🪅🪆🪐🪑🪒🪓🪔🪕🪖🪗🪘🪙"
    "🪚🪛🪜🪝🪞🪟🪠🪡🪢🪣🪤🪥🪦🪧🪨🪰🪱🪲🪳🪴🪵🪶🫀🫁🫂🫐🫑🫒🫓🫔🫕🫖"
)
