import numpy as np


def triangle_color(vector0, vector1, vector2,
                   vector_uv0, vector_uv1, vector_uv2,
                   img, z_array, textures,
                   vector3_normal0, vector3_normal1, vector3_normal2, w, h):
    if vector0[1] == vector1[1] and vector0[1] == vector2[1]:
        return
    if vector0[1] > vector1[1]:
        vector0, vector1 = vector1, vector0
        vector_uv0, vector_uv1 = vector_uv1, vector_uv0
        vector3_normal0, vector3_normal1 = vector3_normal1, vector3_normal0
    if vector0[1] > vector2[1]:
        vector0, vector2 = vector2, vector0
        vector_uv0, vector_uv2 = vector_uv2, vector_uv0
        vector3_normal0, vector3_normal2 = vector3_normal2, vector3_normal0
    if vector1[1] > vector2[1]:
        vector1, vector2 = vector2, vector1
        vector_uv1, vector_uv2 = vector_uv2, vector_uv1
        vector3_normal1, vector3_normal2 = vector3_normal2, vector3_normal1
    total_height = int(vector2[1] - vector0[1])

    for i in range(total_height):
        sec_half = i > vector1[1] - vector0[1] or vector1[1] == vector0[1]
        seg_height = int(vector2[1] - vector1[1]) if sec_half else int(vector1[1] - vector0[1])

        alpha = float(i) / float(total_height)
        beta = float((i - (vector1[1] - vector0[1])) / seg_height) if sec_half else float(i) / float(seg_height)

        vector_a = np.add(vector0, np.multiply(np.subtract(vector2, vector0), alpha))
        vector_b = np.add(vector1, np.multiply(np.subtract(vector2, vector1), beta)) if sec_half else np.add(vector0, np.multiply(
            np.subtract(vector1, vector0), beta))

        vec_uv_a = np.add(vector_uv0, np.multiply(np.subtract(vector_uv2, vector_uv0), alpha))
        vec_uv_a = [int(vec_uv_a[0]), int(vec_uv_a[1])]

        vec_uv_b = np.add(vector_uv1, np.multiply(np.subtract(vector_uv2, vector_uv1), beta)) if sec_half \
            else np.add(vector_uv0, np.multiply(np.subtract(vector_uv1, vector_uv0), beta))

        vec3_norm_a = np.add(vector3_normal0, np.multiply(np.subtract(vector3_normal2, vector3_normal0), alpha))
        vec3_norm_b = np.add(vector3_normal1, np.multiply(np.subtract(vector3_normal2, vector3_normal1), beta)) if sec_half \
            else np.add(vector3_normal0, np.multiply(np.subtract(vector3_normal1, vector3_normal0), beta))

        if vector_a[0] > vector_b[0]:
            vector_a, vector_b = vector_b, vector_a
            vec_uv_a, vec_uv_b = vec_uv_b, vec_uv_a
            vec3_norm_a, vec3_norm_b = vec3_norm_b, vec3_norm_a

        j = int(vector_a[0])
        while j < int(vector_b[0]) + 1:
            phi = 1 if vector_b[0] == vector_a[0] else (j - vector_a[0]) / (vector_b[0] - vector_a[0])

            vec_p = np.add(vector_a, np.multiply(np.subtract(vector_b, vector_a), phi))
            vec_p = [int(vec_p[0]), int(vec_p[1]), int(vec_p[2])]

            vec_uv_p = np.add(vec_uv_a, np.multiply(np.subtract(vec_uv_b, vec_uv_a), phi))
            vec_uv_p = [int(vec_uv_p[0]), int(vec_uv_p[1])]

            vec3_norm_p = np.add(vec3_norm_a, np.multiply(np.subtract(vec3_norm_b, vec3_norm_a), phi))
            vec3_norm_p = normalize(vec3_norm_p)

            light = normalize([0, 0, 3])
            intent = vec3_norm_p[0] * light[0] + vec3_norm_p[1] * light[1] + vec3_norm_p[2] * light[2]

            if intent > 0:
                idx = int(vec_p[0] + vec_p[1] * h)
                if vec_p[0] >= w or vec_p[1] >= h or vec_p[0] < 0 or vec_p[1] < 0:
                    j += 1
                    continue
                if z_array[idx] < vec_p[2]:
                    z_array[idx] = vec_p[2]
                    if 1024 >= (len(textures) - 1 - vec_uv_p[1]) > 0 and 1024 >= vec_uv_p[0] > 0:
                        color = textures[len(textures) - 1 - vec_uv_p[1]][vec_uv_p[0]]
                        img[vec_p[0], vec_p[1]] = [color[0] * intent, color[1] * intent, color[2] * intent]
            j += 1


def scaling(t_array, w, h):
    x_min = np.fabs(np.min(t_array[:, 0]))
    y_min = np.fabs(np.min(t_array[:, 1]))
    z_min = np.fabs(np.min(t_array[:, 2]))

    for i in range(len(t_array)):
        t_array[i, 0] += x_min
        t_array[i, 1] += y_min
        t_array[i, 2] += z_min

    max_xyz = np.maximum(np.fabs(np.max(t_array[:, 0])),
                         np.maximum(np.fabs(np.max(t_array[:, 1])), np.fabs(np.max(t_array[:, 2]))))
    for i in range(len(t_array)):
        t_array[i, 0] = (t_array[i, 0]) * w / max_xyz
        t_array[i, 1] = (t_array[i, 1]) * h / max_xyz
        t_array[i, 2] = (t_array[i, 2]) * 255 / max_xyz

    return np.int32(t_array)


def normalize(n):
    length = 1.0 / (norm(n))
    return np.multiply(n, length)


def viewport(x, y, w, h):
    m = np.eye(4)
    m[0][3] = x + w / 2.
    m[1][3] = y + h / 2.
    m[2][3] = 255 / 2.

    m[0][0] = w / 2.
    m[1][1] = h / 2.
    m[2][2] = 255 / 2.
    return m


def pow_(a, b):
    return [(a[1] * b[2]) - (a[2] * b[1]),
            (a[2] * b[0]) - (a[0] * b[2]),
            (a[0] * b[1]) - (a[1] * b[0])]


def look_at(eye, center, up):
    z = (normalize(np.subtract(eye, center)))
    x = normalize(np.cross(up, z))
    y = normalize(np.cross(z, x))
    min = np.eye(4)
    tr = np.eye(4)
    for i in range(3):
        min[0][i] = x[i]
        min[1][i] = y[i]
        min[2][i] = z[i]
        tr[i][3] = -center[i]
    return np.multiply(min, tr)


def norm(a):
    return np.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
