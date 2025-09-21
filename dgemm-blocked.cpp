const char *dgemm_desc = "Blocked dgemm.";
#include <cstring> // for memcpy
/* This routine performs a dgemm operation
 *  C := C + A * B
 * where A, B, and C are n-by-n matrices stored in row-major format.
 * On exit, A and B maintain their input values. */
void square_dgemm_blocked(int n, int block_size, double *A, double *B, double *C)
{
   // insert your code here
   int N = n / block_size; // number of blocks in one dimension

   // allocate memory for blocks
   double *matrixA = new double[block_size * block_size];
   double *matrixB = new double[block_size * block_size];
   double *matrixC = new double[block_size * block_size];

   for (int i = 0; i < N; i++)
   {
      for (int j = 0; j < N; j++)
      {
         // init block C  as double* matrixC = new double[block_size * block_size];
         int startrowC = i * block_size;
         int startcolC = j * block_size;
         // copy block C from C
         for (int rr = 0; rr < block_size; rr++)
         {
            memcpy(matrixC + rr * block_size,
                   C + (startrowC + rr) * n + startcolC,
                   block_size * sizeof(double));
         }
         // multiply block C with blocks A and B
         for (int k = 0; k < N; k++)
         {
            // load block A as double* matrixA = new double[block_size * block_size];
            int startrowA = i * block_size;
            int startcolA = k * block_size;

            // copy block A from A
            for (int rr = 0; rr < block_size; rr++)
            {
               memcpy(matrixA + rr * block_size,
                      A + (startrowA + rr) * n + startcolA,
                      block_size * sizeof(double));
            }
            // load block B as double* matrixB = new double[block_size * block_size];
            int startrowB = k * block_size;
            int startcolB = j * block_size;

            // copy block B from B
            for (int rr = 0; rr < block_size; rr++)
            {
               memcpy(matrixB + rr * block_size,
                      B + (startrowB + rr) * n + startcolB,
                      block_size * sizeof(double));
            }
            // multiply block C with block A and block B
            for (int ii = 0; ii < block_size; ii++)
            {
               for (int jj = 0; jj < block_size; jj++)
               {
                  for (int kk = 0; kk < block_size; kk++)
                  {
                     matrixC[ii * block_size + jj] +=
                         matrixA[ii * block_size + kk] * matrixB[kk * block_size + jj];
                  }
               }
            }
         }
         // copy block C back to C
         for (int rr = 0; rr < block_size; rr++)
         {
            memcpy(C + (startrowC + rr) * n + startcolC,
                   matrixC + rr * block_size,
                   block_size * sizeof(double));
         }
      }
   }
   // free memory  delete allocated memory
   delete[] matrixA;
   delete[] matrixB;
   delete[] matrixC;
}