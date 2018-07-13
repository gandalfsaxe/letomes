@jit
def symplectic_euler_step1(h,x,y,px,py):
    # Step 1
    Fx,Fy = F(x,y)
    vpx = Fx+py
    px = (px+(vpx+Fy*h)*h)/(1.0+h*h)
    vpy = Fy-px
    py += vpy*h
    # Step 2
    vx = px+y
    vy = py-x
    x += vx*h
    y += vy*h
    return x,y,px,py

@jit
def symplectic_euler_step2(h,x,y,px,py):
    # Step 1
    Fx,Fy = F(x,y)
    vpx = Fx+py
    vpy = Fy-px
    px += vpx*h
    py += vpy*h
    # Step 2
    vx = px+y
    x = (x+(vx+py*h)*h)/(1.0+h*h)
    vy = py-x
    y += vy*h
    return x,y,px,py

@jit
def symplectic_verlet_step2(h,x,y,px,py):
    hh = 0.5*h
    denum = 1.0/(1.0+hh*hh)
    # Step 1
    Fx,Fy = F(x,y)
    vpx = Fx+py
    px = (px+(vpx+Fy*hh)*hh)*denum
    vpy = Fy-px
    py += vpy*hh
    # Step 2
    vx = px+y
    vy = py-x
    x = (x+(2.0*vx+(vy+py)*hh)*hh)*denum
    y += (vy+py-x)*hh
    # Step 3
    Fx,Fy = F(x,y)
    vpx = Fx+py
    vpy = Fy-px
    px += vpx*hh
    py += vpy*hh
    return x,y,px,py