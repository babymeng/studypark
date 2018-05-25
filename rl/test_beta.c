#include <stdlib.h>
#include "gen_beta.h"
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <time.h>
#include <unistd.h>	/* used for getpid to initialize random */
void test_beta(double a, double b, int c)
{
    int i;
    clock_t start_time,     stop_time;
    
    double x;
    double sum=0, sum2=0, count=0;
    double var, expected_mean, expected_sq;
    
    gen_beta_param g;
    
    start_time = clock();
    gen_beta_initialize(&g, a,b);
    
    for (i=0; i<c; i++)
    {   x = gen_beta(&g);
        assert(x>=0);
	assert(x<=1);
	sum += x;
	sum2+= x*x;
	count ++;
    }
    stop_time = clock();
    
    var = (count*sum2-sum*sum)/(count*(count-1));
    
    expected_mean = a/(a+b);
    expected_sq = a*(a+1)/ (a+b)/(a+b+1);
    
    printf("For beta(%g,%g), sample of %g, %g microseconds/sample\n",	
    	a,b, count, (stop_time-start_time+0.0)/count);
    printf("mean= %g, expected mean=%g\n", sum/count, expected_mean);
    printf("mean square= %g, expected mean square=%g\n", 
    	sum2/count, expected_sq);
    printf("\n");
}


int main()
{
    srandom(getpid());
    // test_beta(1.0e-35, 0.1, 2000000);
    // test_beta(0.1, 1.0e-35, 2000000);

    // test_beta(0.5, 0.5, 4000000);
    // 

    // test_beta(1.0e-8, 1.3e-7, 2000000);
    // test_beta(1.3e-7, 1.0e-8, 2000000);
    // 
    // test_beta(0.499, 0.499, 1000000);
    // test_beta(0.501, 0.501, 1000000);

    // test_beta(0.499, 0.501, 2000000);
    // test_beta(0.501, 0.499, 2000000);
    // 
    // test_beta(1.0e-38, 1.3e-37, 2000000);
    // test_beta(1.3e-37, 1.0e-38, 2000000);

    // test_beta(10.0, 1.3, 2000000);
    // test_beta(1.3, 10.0, 2000000);
    // 
    // test_beta(100., 200., 2000000);
    // test_beta(200., 100., 2000000);
    // 
    // test_beta(1e30, 2e30, 2000000);
    // test_beta(2e30, 1e30, 2000000);
    // 
    // test_beta(1.4, 0.3, 2000000);
    // test_beta(0.3, 1.4, 2000000);
    // 
    // test_beta(1e20, 1e-20, 2000000);
    // test_beta(1e-20, 1e20, 2000000);
    // 
    // test_beta(0.9, 0.3, 2000000);
    // test_beta(0.3, 0.9, 2000000);

    // test_beta(0.4, 0.3, 2000000);
    // test_beta(0.3, 0.4, 2000000);

    // test_beta(1e-20, 0.03, 2000000);
    // test_beta(0.03, 1e-20, 2000000);
    
    gen_beta_param g;
    gen_beta_initialize(&g, 100,200);
    double x;
    for (int i = 0; i < 10; i++) {
	//start_time = clock();
	x = gen_beta(&g);
	printf("%g,",x);
    }

}
