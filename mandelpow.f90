! Mandelbrot with arbitrary power
!##############################################################################!

module mandelpow

  implicit none

  contains !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  subroutine main( pow, z0, max_iter, max_value, out )

    implicit none

    ! variable declarations
    !++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++!

    ! input arguments
    !..........................................................................!

    integer( 4 ), intent( in ) :: max_iter

    real( 4 ), intent( in ) :: pow, max_value

    complex( 8 ), intent( in ) :: z0

    ! output arguments
    !..........................................................................!

    integer( 4 ), intent( inout ) :: out( :, : )

    ! internal variables
    !..........................................................................!
    complex( 8 ) :: c, z

    integer( 4 ) :: N, i, j, s

    ! variable initializations
    !++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++!

    N = size( out, 1 )

    out = max_iter

    !$omp parallel do default(none) &
    !$omp& shared(pow, z0, max_iter, max_value, N, out) &
    !$omp& private(s, i, j, z, c)

    do i = 1, N
      do j = 1, N

        z = z0
        c = cmplx( 4. * float( i ) / ( N - 1. ) - 2, 4. * float( j ) / ( N - 1. ) - 2 )

        do s = 0, max_iter
          if ( abs( z ) > max_value) then
            out( i, j ) = s
            exit
          else
            z = z ** pow + c
          end if
        end do

      end do
    end do

  end subroutine main

end module mandelpow

!##############################################################################!