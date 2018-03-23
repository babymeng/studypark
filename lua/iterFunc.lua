tlist = {[4] = "4D", [1] = "1A", [5] = "5E", [2] = "2B", [0] = "00",}

local function pairsByKey(tDict)
    local tmp = {}
    for i in pairs(tDict) do
        tmp[#tmp + 1] = i
    end
    table.sort(tmp)

    local j = 0
    return function ()
        j = j + 1
        return tmp[j], tDict[tmp[j]]
    end
end


for key, value in pairsByKey(tlist) do
    print("key = " .. key .. " value = " .. value)
end
