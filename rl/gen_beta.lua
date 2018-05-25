local _M = {}

_M._VERSION = "1.0"

local mt = { __index__ = _M }

function _M.new(self)
    return setmetatable({a = 0.0,b = 0.0,min_ab = 0.0,max_ab = 0.0,sum_ab = 0.0,param  = {0.0, 0.0}}, mt)
end

local FLT_MAX = 3.40282347e+38

function _M.gen_beta_initialize(self, a, b)
    local t = 0.0

    if a <= 0 or b <= 0 then return end
    self.a = a
    self.b = b

    if a < b then
        self.min_ab = a
        self.max_ab = b
    else
        self.min_ab = b
        self.max_ab = a
    end
    self.sum_ab = a + b

    if self.min_ab > 1.0 then
        self.param[1] = math.sqrt((self.sum_ab - 2.0)/(2.0 * a * b - self.sum_ab))
        self.param[2] = self.min_ab + 1.0 / self.param[1]
    elseif self.max_ab > 1.0 then
        t = (1 - self.min_ab)/(1 + self.max_ab - self.min_ab)
        self.param[1] = t
        self.param[2] = self.max_ab * t / (self.max_ab * t + self.min_ab * math.pow(1 - self.param[1], self.max_ab))
    else
        if self.min_ab == 1.0 then
            self.param[1] = 0.5
            self.param[2] = 0.5
        else
            t = 1 / (1 + math.sqrt(self.max_ab * (1 - self.max_ab)/(self.min_ab * (1 - self.min_ab))))
            self.param[1] = t
            self.param[2] = self.max_ab * t / (self.max_ab * t + self.min_ab * (1 - t))
        end
    end
end

local function aexp(a, v)
    if v > 88.7 then
        return FLT_MAX
    else
        return a * math.exp(v)
    end
end

local function ret(a, mina, b, w)
    if a == mina then
        return w/(b+w)
    else
        return b/(b+w)
    end
end

local function DRAND()
    --math.randomseed(tostring(os.time()):reverse():sub(1, 6))
    return math.random()
end

function _M.gen_beta(self)
    --local DRAND = ((math.random()+0.5)/2147483648.0)
    local c,r,s,t,u1,u2,v,w,z,lambda = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
    local logv, logw, log_sum = 0.0,0.0,0.0

    local a = self.a
    local b = self.b
    local min_ab = self.min_ab
    local max_ab = self.max_ab
    local sum_ab = self.sum_ab

    if (min_ab > 1.0) then
        lambda = self.param[1]
        c = self.param[2]
        repeat
            u1 = DRAND()
            u2 = DRAND()
            v = lambda*math.log(u1/(1.0-u1))
            w = aexp(min_ab,v)
            z = u1*u1*u2
            r = c*v-1.38629436112
            s = min_ab+r-w
            if(s+2.609438 >= 5.0*z) then break end
            t = math.log(z)
        until (r+sum_ab*math.log(sum_ab/(max_ab+w)) < t)
        print("w=".. tostring(w))
        print("lambda=".. tostring(lambda))
        print("u1=".. tostring(u1))
        print("math.log(u1/(1.0-u1))=".. tostring(math.log(u1/(1.0-u1))))
        print("v=".. tostring(v))
        return ret(a,min_ab, max_ab, w)
    end

    print("---------------------")
    if (max_ab>= 1.0) then
        t = self.param[1]
        r = self.param[2]
        while true do
            u1 = DRAND()
            u2 = DRAND()
            if u1 < r then
                w = t*math.pow(u1/r, 1/min_ab)
                if (math.log(u2) < (max_ab -1)*math.log((1-w)/(1-t))) then break end
            else
                w = 1- (1-t)*math.pow((1-u1)/(1-r), 1/max_ab)
                if (math.log(u2) < (min_ab -1) * math.log(w/t)) then break end
            end
        end
        
        if (a==min_ab) then
            return w
        else
            return 1-w
        end
    end
end

return _M
