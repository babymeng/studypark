local gen_beta = require 'gen_beta'

local g = gen_beta.new()
gen_beta.gen_beta_initialize(g,100,200)
--[[
print("g.a=" .. tostring(g.a))
print("g.b=" .. tostring(g.b))
print("g.sum_ab=" .. tostring(g.sum_ab))
print("g.max_ab=" .. tostring(g.max_ab))
print("g.min_ab=" .. tostring(g.min_ab))
print("g.param[1]=" .. tostring(g.param[1]))
print("g.param[2]=" .. tostring(g.param[2]))
--]]

local x = 0.0

for i=0, 10, 1 do
    x = gen_beta.gen_beta(g)
    print(x)
end
