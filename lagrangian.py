# Request Data is the most important function. It takes the input (vtkImageData), does all the computatoin and returns the output (vtkImageData)
def RequestData(self, request, inInfo, outInfo):
    xs = np.linspace(0.0, 2.0, self.Dimensions[0])
    ys = np.linspace(0.0, 1.0, self.Dimensions[1])
    ts = np.linspace(0.0, 15.0, self.Dimensions[2])
    x, y, t = np.meshgrid(xs, ys, ts, indexing="ij")

    output = vtkImageData.GetData(outInfo, 0)
    output.SetDimensions(self.Dimensions)
    output.SetSpacing(abs(xs[1] - xs[0]), abs(ys[1] - ys[0]), abs(ts[1] - ts[0]))
    output.SetOrigin(xs[0], ys[0], ts[0])
    output = dsa.WrapDataObject(output)

    if self.Vectorize:
        print(self.T, self.A, self.eps)
        start = timer()
        v = self.double_gyre_vectorized(x, y, t)
        end = timer()
        print("Vectorized time: {}s".format(end - start))
    else:
        start = timer()
        v = self.double_gyre_loop(x, y, t)
        end = timer()
        print("Loop time: {}s".format(end - start))

    output.PointData.append(v.reshape((-1, 3), order="F"), "v")
    output.VTKObject.GetPointData().SetActiveScalars("v")

    return 1
