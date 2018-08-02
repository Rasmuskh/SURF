//=============================================================================
// TypesAndConsts.h
//=============================================================================
// abstraction.......Basic types and Constants for CornerStone130 Device
// class.............Basic structures
// original author...S. MINOLLI - NEXEYA
//=============================================================================

#ifndef _TYPES_AND_CONSTS_H_
#define _TYPES_AND_CONSTS_H_

//=============================================================================
// DEPENDENCIES
//=============================================================================
#include <vector>
#include <map>


namespace CornerStone130_ns
{

//- Shutter state
typedef enum
{
	E_CLOSED = 0,
	E_OPENED, 
	E_NONE
} E_shutter_state_t;

//- Grating definition
typedef struct GratingDef
{
  //- members --------------------
  std::string label; // grating label

  double minWaveLength; // min wave length in user unit

  double maxWaveLength; // max wave length in user unit

  //- default constructor -----------------------
  GratingDef ()
    : label(""),
    minWaveLength(yat::IEEE_NAN),
    maxWaveLength(yat::IEEE_NAN)
  {
  }

  //- destructor -----------------------
  ~GratingDef ()
  {
  }

  //- copy constructor ------------------
  GratingDef (const GratingDef& src)
  {
    *this = src;
  }

  //- operator= ------------------
  const GratingDef & operator= (const GratingDef& src)
  {
      if (this == & src) 
        return *this;

      this->label = src.label;
      this->minWaveLength = src.minWaveLength;
      this->maxWaveLength = src.maxWaveLength;

      return *this;
  }

  //- dump -----------------------
  void dump () const
  {
    std::cout << "GratingDef::label........." 
              << this->label
              << std::endl; 
    std::cout << "GratingDef::minWaveLength........." 
              << this->minWaveLength
              << std::endl; 
    std::cout << "GratingDef::maxWaveLength........." 
              << this->maxWaveLength
              << std::endl;
  }

} GratingDef;

//- List of <KEY, value> defining the filters:
//- KEY = filter id
//- value = filter label
typedef std::pair<yat::uint16, std::string> Filters_pair_t;
typedef std::map<yat::uint16, std::string> Filters_t;
typedef Filters_t::iterator Filters_it_t;

//- List of <KEY, value> defining the gratings:
//- KEY = grating id
//- value = grating definition
typedef std::pair<yat::uint16, GratingDef> Gratings_pair_t;
typedef std::map<yat::uint16, GratingDef> Gratings_t;
typedef Gratings_t::iterator Gratings_it_t;

} //- namespace CornerStone130_ns

#endif //- _TYPES_AND_CONSTS_H_

