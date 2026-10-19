"""
The fixed 256-entry emoji table that emojihash indexes into.

Every entry is a single code point at or above U+1F300 with default emoji presentation, so
no variation selector or ZWJ sequence is needed and each renders as one glyph. All entries
are from Emoji 12.0 or earlier for broad font support.

The order is part of the output contract: reordering, adding, or removing entries changes
the emoji every input maps to.
"""

EMOJI: tuple[str, ...] = tuple(
    "🐀🐂🐄🐅🐇🐉🐊🐋🐌🐍🐎🐐🐑🐒🐓🐕"
    "🐖🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐦🐧🐨"
    "🐪🐫🐬🐭🐯🐱🐸🐺🐻🐼🦀🦁🦂🦃🦄🦅"
    "🦆🦇🦈🦉🦊🦋🦌🦍🦎🦏🦐🦑🦒🦓🦔🦕"
    "🦖🦗🦘🦙🦚🦛🦜🦝🦞🦟🦡🦢🦥🦦🦧🦨"
    "🦩🌰🌱🌲🌳🌴🌵🌷🌸🌹🌺🌻🌼🌽🌾🍀"
    "🍁🍂🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍐🍑🍒"
    "🍓🍔🍕🍖🍗🍛🍜🍝🍞🍟🍣🍤🍦🍩🍪🍫"
    "🍬🍭🍯🍰🍳🍷🍸🍹🍺🥐🥑🥒🥓🥔🥕🥖"
    "🥗🥚🥛🥜🥝🥞🥟🥥🥦🥨🥩🥪🥭🧀🧁🧄"
    "🧅🧊🌀🌂🌈🌊🌋🌍🌙🌞🌟🎀🎁🎂🎃🎄"
    "🎈🎉🎒🎓🎠🎡🎢🎣🎤🎧🎨🎩🎪🎫🎬🎭"
    "🎮🎯🎲🎳🎷🎸🎹🎺🎻🎾🏀🏆🏈🏓🏠🏰"
    "🔑🔒🔔🔥🔦🔧🔨🔩🔬🔭🔮💎💡💣💰💾"
    "💿📌📎📏📚📜📡📦📫📷📺📻🚀🚁🚂🚌"
    "🚑🚒🚓🚕🚗🚚🚜🚢🚤🚦🚧🚨🛵🛶🛸🛹"
)
