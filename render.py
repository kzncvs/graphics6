from core import triangle_color, scaling
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Pi


def parsing_obj(obj_link):
    obj_file = open(obj_link)
    vertices = []
    texture_vertices = []
    vertex_normals = []
    faces_coordinates = []
    faces_textures = []
    faces_vec_normals = []
    for line in obj_file:
        split_line = line.replace('\n', '').split(' ')
        if split_line[0] == 'v':
            vertices.append([float(i) for i in split_line[1:4]])
        elif split_line[0] == 'vt':
            texture_vertices.append([float(i) for i in split_line[2:4]])
        elif split_line[0] == 'vn':
            vertex_normals.append([float(i) for i in split_line[2:5]])
        elif split_line[0] == 'f':
            faces_coordinates.append([int(split_line[index + 1].split('/')[0]) for index in range(3)])
            faces_textures.append([int(split_line[index + 1].split('/')[1]) for index in range(3)])
            faces_vec_normals.append([int(split_line[index + 1].split('/')[2]) for index in range(3)])
    return faces_textures, vertex_normals, faces_vec_normals, vertices, texture_vertices, faces_coordinates


def main_activity(w, h, obj_link, tga_link):
    faces_textures, vertex_normals, faces_vec_normals, vertices, texture_vertices, faces_coordinates = \
        parsing_obj(obj_link)
    textures = np.array(Pi.open(tga_link))
    image = np.zeros(shape=(h + 1, w + 1, 3)).astype(np.uint8)

    n_pass = scaling(np.array([[k[0], k[1], k[2]] for k in vertices]), w, h)
    z_array = [np.iinfo(np.int32).min for _ in range(h * w)]

    # vec_p - triangles index
    # vec_p1 - texture index
    # vec_p2 - norm vector index
    k = 0
    for vec_p, vec_p1, vec_p2 in zip(faces_coordinates, faces_textures, faces_vec_normals):
        vec3_int = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        vec3_norm = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        vec_uv = [[0, 0], [0, 0], [0, 0]]

        for i in range(3):
            vec3_int[i] = [h - 1 - n_pass[vec_p[i] - 1, 1],
                           n_pass[vec_p[i] - 1, 0],
                           n_pass[vec_p[i] - 1, 2]]
            vec_uv[i] = [int(texture_vertices[vec_p1[i] - 1][0] * len(textures)),
                         int(texture_vertices[vec_p1[i] - 1][1] * len(textures))]
            vec3_norm[i] = [vertex_normals[vec_p2[i] - 1][0], vertex_normals[vec_p2[i] - 1][1],
                            vertex_normals[vec_p2[i] - 1][2]]

        triangle_color(vec3_int[0], vec3_int[1], vec3_int[2],  # triangles
                       vec_uv[0], vec_uv[1], vec_uv[2],
                       image, z_array, textures,
                       vec3_norm[0], vec3_norm[1], vec3_norm[2], w, h)  # textures
        k += 1
    return np.uint8(image)


def show_image(image):
    plt.imshow(image, cmap="gray", interpolation="none")
    plt.show()
