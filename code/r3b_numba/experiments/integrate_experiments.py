@jit
def symplectic_euler_step1(h, x, y, p_x, p_y):
    # Step 1
    Fx, Fy = F(x, y)
    pdot_x = Fx + p_y
    p_x = (p_x + (pdot_x + Fy * h) * h) / (1.0 + h * h)
    pdot_y = Fy - p_x
    p_y += pdot_y * h
    # Step 2
    v_x = p_x + y
    v_y = p_y - x
    x += v_x * h
    y += v_y * h
    return x, y, p_x, p_y


@jit
def symplectic_euler_step2(h, x, y, p_x, p_y):
    # Step 1
    Fx, Fy = F(x, y)
    pdot_x = Fx + p_y
    pdot_y = Fy - p_x
    p_x += pdot_x * h
    p_y += pdot_y * h
    # Step 2
    v_x = p_x + y
    x = (x + (v_x + p_y * h) * h) / (1.0 + h * h)
    v_y = p_y - x
    y += v_y * h
    return x, y, p_x, p_y


@jit
def symplectic_verlet_step2(h, x, y, p_x, p_y):
    hh = 0.5 * h
    denum = 1.0 / (1.0 + hh * hh)
    # Step 1
    Fx, Fy = F(x, y)
    pdot_x = Fx + p_y
    p_x = (p_x + (pdot_x + Fy * hh) * hh) * denum
    pdot_y = Fy - p_x
    p_y += pdot_y * hh
    # Step 2
    v_x = p_x + y
    v_y = p_y - x
    x = (x + (2.0 * v_x + (v_y + p_y) * hh) * hh) * denum
    y += (v_y + p_y - x) * hh
    # Step 3
    Fx, Fy = F(x, y)
    pdot_x = Fx + p_y
    pdot_y = Fy - p_x
    p_x += pdot_x * hh
    p_y += pdot_y * hh
    return x, y, p_x, p_y

