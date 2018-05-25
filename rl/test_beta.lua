local ffi = require 'ffi'

local beta = ffi.load('gen_beta.so')

ffi.cdef[[
    typedef struct _gen_beta_param
    {   
        double a,b;     /* the parameters of the beta distribution */
        /* The remaining fields are precomputed values that can
         * save some computation when many numbers are drawn from the
         * same distribution.
         */
        double min_ab, max_ab;  /* min(a,b) and max(a,b) */
        double sum_ab;          /* a+b */
        double param[3];        /* various precomputed parameters,
                                 * different for each generation method
                                 */
    } gen_beta_param;

    void gen_beta_initialize(gen_beta_param *gen, double a, double b); 
    double gen_beta(const gen_beta_param *gen);
    int printf(const char *fmt, ...);
]]

local g = ffi.new("gen_beta_param")
beta.gen_beta_initialize(g, 100, 200)
local x = ffi.typeof("double")

for i=0,10,1 do
    x = beta.gen_beta(g)
    ffi.C.printf("%g,\n",x)
end


