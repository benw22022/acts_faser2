// This file is part of the ACTS project.
//
// Copyright (C) 2016 CERN for the benefit of the ACTS project
//
// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#pragma once

#include "Acts/Geometry/TrackingGeometry.hpp"
#include "Acts/Utilities/BinUtility.hpp"
#include "Acts/Utilities/BinningType.hpp"
#include "ActsExamples/Faser2TelescopeDetector/Faser2TelescopeDetectorElement.hpp"

#include <array>
#include <memory>
#include <vector>

namespace Acts {
class TrackingGeometry;
}  // namespace Acts

namespace ActsExamples::Faser2Telescope {

/// The Faser2Telescope detector surface type
enum class Faser2TelescopeSurfaceType {
  Plane = 0,
  Disc = 1,
};

/// Global method to build the Faser2Telescope tracking geometry
///
/// @param gctx is the detector element dependent geometry context
/// @param detectorStore is the store for the detector element
/// @param positions are the positions of different layers in the longitudinal
///                  direction
/// @param stereoAngles are the stereo angles of different layers, which are
///                     rotation angles around the longitudinal (normal)
///                     direction
/// @param offsets is the offset (u, v) of the layers in the transverse plane
/// @param bounds is the surface bound values, i.e. halfX and halfY if plane
///               surface, and minR and maxR if disc surface
/// @param thickness is the material thickness of each layer
/// @param boundsX is the surface bound values in X direction for each layer
/// @param boundsY is the surface bound values in Y direction for each layer
/// @param Type_surf is the surface type of each layer
/// @param surfaceType is the detector surface type
/// @param binValue indicates which axis the detector surface normals are
/// parallel to
std::unique_ptr<const Acts::TrackingGeometry> buildDetector(
    const typename Faser2TelescopeDetectorElement::ContextType& gctx,
    std::vector<std::shared_ptr<Faser2TelescopeDetectorElement>>& detectorStore,
    const std::vector<double>& positions,
    const std::vector<double>& stereoAngles,
    const std::array<double, 2>& offsets, const std::array<double, 2>& bounds,
    double thickness,const std::vector<double>& boundsX, const std::vector<double>& boundsY,const std::vector<int>& Type_surf,
    Faser2TelescopeSurfaceType surfaceType,
    Acts::BinningValue binValue = Acts::BinningValue::binZ);

}  // namespace ActsExamples::Faser2Telescope
