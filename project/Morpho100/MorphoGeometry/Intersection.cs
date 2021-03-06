﻿using System;
using System.Collections.Generic;

namespace MorphoGeometry
{
    public class Intersection
    {

        public static Vector RayFaceIntersect(Ray ray, Face face, bool reverse = false, bool project = false)
        {
            Vector v0, v1, v2;

            if (reverse)
            {
                v1 = face.A;
                v0 = face.B;
                v2 = face.C;
            }
            else
            {
                v0 = face.A;
                v1 = face.B;
                v2 = face.C;
            }

            Vector v0v1 = v1.Sub(v0);
            Vector v0v2 = v2.Sub(v0);
            Vector pvec = ray.direction.Cross(v0v2);
            float det = v0v1.Dot(pvec);

            if (det < 0.000001)
                return null;

            float invDet = (float)(1.0 / det);
            Vector tvec = ray.origin.Sub(v0);
            float u = tvec.Dot(pvec) * invDet;

            if (u < 0 || u > 1)
                return null;

            Vector qvec = tvec.Cross(v0v1);
            float v = ray.direction.Dot(qvec) * invDet;

            if (v < 0 || u + v > 1)
                return null;

            float distance = (v0v2.Dot(qvec) * invDet);
            float c = (float) Math.Sqrt(ray.direction.x * ray.direction.x + ray.direction.y * ray.direction.y + ray.direction.z * ray.direction.z);
            float angle = distance / c;

            Vector intersection = new Vector(ray.origin.x + ray.direction.x * angle, ray.origin.y + ray.direction.y * angle, ray.origin.z + ray.direction.z * angle);

            if (project)
                intersection = new Vector(ray.origin.x, ray.origin.y, ray.origin.z);

            return intersection;
        }

        public static IEnumerable<Vector> RaysFaceGroupIntersect(List<Ray> rays, FaceGroup facegroup, bool reverse = false, bool project = false)
        {
            List<Vector> intersections = new List<Vector>();

            Vector intersection;
            foreach (Face face in facegroup.Faces)
                foreach (Ray ray in rays)
                {
                    intersection = RayFaceIntersect(ray, face, reverse, project);
                    if (intersection != null)
                        intersections.Add(intersection);
                }

            return intersections;
        }

    }
}
