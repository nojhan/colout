def theme(context):

    return context,[
        ["^    (Start)(.*): (.*):(.*)$", "yellow", "normal,normal,normal,bold"], # Test start.
        #          path  file ext:line    :
        ["^(tests): (/.*?)/([^/:]+):([0-9]+): (.*)", "yellow,none,white,yellow,red", "bold,normal,bold,normal,bold"],
        ["(`)(.*)('.*)", "red,Cpp,red", "bold,normal,bold"],
        ["^\.+$", "yellow", "bold"],
        ["^=+$", "yellow", "bold"],
        ["(/.*?)/([^/:]+):([0-9]+): (FAILED):", "white,white,yellow,red", "normal,bold,normal,bold"],
        ["(REQUIRE\(|CHECK\(|REQUIRE_THAT\()(.*)(\))$","yellow,Cpp,yellow","bold,normal,bold"],
        # Hide uninteresting stuff:
        ["[0-9]+/[0-9]+ Test.*","blue"],
        ["^Filters:.*","blue"],
        ["^Randomness seeded to:.*","blue"],
        ["^tests is a Catch2.*","blue"],
        ["^Run with.*", "blue"],
        ["^~+$","blue"],
        ["^-+$","blue"],
        ["^\s*(Scenario:|Given:|When:|Then:).*","blue"],
        ["^(/.*?)/([^/:]+):([0-9]+)", "blue"],
        ["^(test cases|assertions)(.*)", "blue"],
    ]
