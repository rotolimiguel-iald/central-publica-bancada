    1/*
    2 * Copyright (C) 2014, 2016 Karl Wette
    3 * Copyright (C) 2009-2013 Adam Mercer
    4 *
    5 * This program is free software; you can redistribute it and/or modify
    6 * it under the terms of the GNU General Public License as published by
    7 * the Free Software Foundation; either version 2 of the License, or (at
    8 * your option) any later version.
    9 *
   10 * This program is distributed in the hope that it will be useful, but
   11 * WITHOUT ANY WARRANTY; without even the implied warranty of
   12 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   13 * General Public License for more details.
   14 *
   15 * You should have received a copy of the GNU General Public License
   16 * along with with program; see the file COPYING. If not, write to the
   17 * Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
   18 * MA 02110-1301 USA
   19 */
   20 
   21/*
   22 * LALSimulationVCSInfo.h - LALSimulation VCS Information Header
   23 */
   24 
   25/** \cond DONT_DOXYGEN */
   26 
   27#ifndef _LALSIMULATIONVCSINFOHEADER_H
   28#define _LALSIMULATIONVCSINFOHEADER_H
   29 
   30#include <lal/LALVCSInfoType.h>
   31#include <lal/LALSimulationVCSInfo.h>
   32#include <lal/LALSimulationConfig.h>
   33 
   34#ifdef __cplusplus
   35extern "C" {
   36#endif
   37 
   38/* VCS information */
   39#define LALSIMULATION_VCS_ID "2c00d8c200308422036d0a23b7c0394f7c73faad"
   40#define LALSIMULATION_VCS_DATE "2026-06-13 10:50:52 +0000"
   41#define LALSIMULATION_VCS_BRANCH "None"
   42#define LALSIMULATION_VCS_TAG "lalsuite-v7.26.15"
   43#define LALSIMULATION_VCS_AUTHOR "Karl Wette <karl.wette@ligo.org>"
   44#define LALSIMULATION_VCS_COMMITTER "Karl Wette <karl.wette@ligo.org>"
   45#define LALSIMULATION_VCS_CLEAN "CLEAN"
   46#define LALSIMULATION_VCS_STATUS "CLEAN: All modifications committed"
   47 
   48#if LALSIMULATION_VERSION_DEVEL != 0
   49/* VCS header/library mismatch link check function */
   50#define LALSIMULATION_VCS_LINK_CHECK LALSIMULATION_CLEAN_2c00d8c200308422036d0a23b7c0394f7c73faad_VCS_HEADER_LIBRARY_MISMATCH
   51void LALSIMULATION_VCS_LINK_CHECK(void);
   52#endif
   53 
   54#ifdef __cplusplus
   55}
   56#endif
   57 
   58#endif /* _LALSIMULATIONVCSINFOHEADER_H */
   59 
   60/** \endcond */
