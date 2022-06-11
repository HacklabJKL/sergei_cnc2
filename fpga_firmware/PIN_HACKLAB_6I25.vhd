library IEEE;
use IEEE.std_logic_1164.all;  -- defines std_logic types
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Copyright (C) 2007, Peter C. Wallace, Mesa Electronics
-- http://www.mesanet.com
--
-- This program is is licensed under a disjunctive dual license giving you
-- the choice of one of the two following sets of free software/open source
-- licensing terms:
--
--    * GNU General Public License (GPL), version 2.0 or later
--    * 3-clause BSD License
-- 
--
-- The GNU GPL License:
-- 
--     This program is free software; you can redistribute it and/or modify
--     it under the terms of the GNU General Public License as published by
--     the Free Software Foundation; either version 2 of the License, or
--     (at your option) any later version.
-- 
--     This program is distributed in the hope that it will be useful,
--     but WITHOUT ANY WARRANTY; without even the implied warranty of
--     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--     GNU General Public License for more details.
-- 
--     You should have received a copy of the GNU General Public License
--     along with this program; if not, write to the Free Software
--     Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
-- 
-- 
-- The 3-clause BSD License:
-- 
--     Redistribution and use in source and binary forms, with or without
--     modification, are permitted provided that the following conditions
--     are met:
-- 
--   * Redistributions of source code must retain the above copyright
--     notice, this list of conditions and the following disclaimer.
-- 
--   * Redistributions in binary form must reproduce the above
--     copyright notice, this list of conditions and the following
--     disclaimer in the documentation and/or other materials
--     provided with the distribution.
-- 
--   * Neither the name of Mesa Electronics nor the names of its
--     contributors may be used to endorse or promote products
--     derived from this software without specific prior written
--     permission.
-- 
-- 
-- Disclaimer:
-- 
--     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
--     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
--     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
--     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
--     COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
--     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
--     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
--     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
--     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
--     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
--     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
--     POSSIBILITY OF SUCH DAMAGE.
-- 

use work.IDROMConst.all;

package PIN_HACKLAB_6I25 is
	constant ModuleID : ModuleIDType :=( 
	 -- ModuleTag     Version  ClockType     Instances BaseAddr                   NumRegisters         Strides  MultRegs
		(WatchDogTag,	x"00",	ClockLowTag,	x"01",	WatchDogTimeAddr&PadT,		WatchDogNumRegs,		x"00",	WatchDogMPBitMask),
		(IOPortTag,		x"00",	ClockLowTag,	x"02",	PortAddr&PadT,					IOPortNumRegs,			x"00",	IOPortMPBitMask),
		(PWMTag,			x"00",	ClockHighTag,	x"04",	PWMValAddr&PadT,				PWMNumRegs,				x"00",	PWMMPBitMask),
		(QcountTag,		x"02",	ClockLowTag,	x"03",	QcounterAddr&PadT,			QCounterNumRegs,		x"00",	QCounterMPBitMask),
		(StepGenTag,	x"02",	ClockLowTag,	x"01",	StepGenRateAddr&PadT,		StepGenNumRegs,		x"00",	StepGenMPBitMask),
		(LEDTag,			x"00",	ClockLowTag,	x"01",	LEDAddr&PadT,					LEDNumRegs,				x"00",	LEDMPBitMask),
		(RCPWMTag,		x"00",	ClockLowTag,		x"01",	RCPWMWidthAddr&PadT,			RCPWMNumRegs,			x"00",	RCPWMMPBitMask),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000"),
		(NullTag,		x"00",	NullTag,			x"00",	NullAddr&PadT,					x"00",					x"00",	x"00000000")
		);
		
	
	constant PinDesc : PinDescType :=(
		-- External DB25, Port 1
-- 	Base func  sec unit sec func 	 sec pin		
		IOPortTag & x"00" & PWMTag    & PWMAOutPin,			-- I/O 00 / Pin  1:	X_FWD	
		IOPortTag & x"00" & NullTag   & x"00",				-- I/O 01 / Pin 14: GPIO / MOTOR_FAULT
		IOPortTag & x"00" & PWMTag    & PWMBDirPin,			-- I/O 02 / Pin  2:	X_REV
		IOPortTag & x"00" & NullTag   & x"00",				-- I/O 03 / Pin 15: GPIO / X_HOME
		IOPortTag & x"00" & QCountTag & QCountQAPin,		-- I/O 04 / Pin  3: X_A
		IOPortTag & x"00" & NullTag   & x"00",				-- I/O 05 / Pin 16: GPIO / Y_HOME
		IOPortTag & x"00" & QCountTag & QCountQBPin,		-- I/O 06 / Pin  4: X_B
		IOPortTag & x"00" & NullTag   & x"00",				-- I/O 07 / Pin 17: GPIO / Z_HOME
		IOPortTag & x"01" & PWMTag    & PWMAOutPin,			-- I/O 08 / Pin  5:  Y_FWD
		IOPortTag & x"01" & PWMTag    & PWMBDirPin,			-- I/O 09 / Pin  6:  Y_REV
		IOPortTag & x"01" & QCountTag & QCountQAPin,		-- I/O 10 / Pin  7:  Y_A
		IOPortTag & x"01" & QCountTag & QCountQBPin,		-- I/O 11 / Pin  8:  Y_B
		IOPortTag & x"00" & RCPWMTag  & RCPWMOutPin,		-- I/O 12 / Pin  9:  Z_PWM
		IOPortTag & x"02" & NullTag   & x"00",				-- I/O 13 / Pin 10:  
		IOPortTag & x"02" & QCountTag & QCountQAPin,		-- I/O 14 / Pin 11:  Z_A
		IOPortTag & x"02" & QCountTag & QCountQBPin,		-- I/O 15 / Pin 12:  Z_B
		IOPortTag & x"00" & NullTag   & x"00",				-- I/O 16 / Pin 13:  GPIO / MOTOR_HCURR

		-- Internal 26 pin header, Port 2
		IOPortTag & x"00" & StepGenTag & StepGenStepPin,	-- I/O 17 / Pin  1: Rotary axis step
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 18 / Pin 14
		IOPortTag & x"00" & StepGenTag & StepGenDirPin,		-- I/O 19 / Pin  2: Rotary axis dir
		IOPortTag & x"00" & NullTag    & x"00",			-- I/O 20 / Pin 15: FET1_CTRL
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 21 / Pin  3
		IOPortTag & x"00" & NullTag    & x"00",			-- I/O 22 / Pin 16: FET2_CTRL
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 23 / Pin  4
		IOPortTag & x"00" & NullTag    & x"00",			-- I/O 24 / Pin 17: FET3_CTRL
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 25 / Pin  5
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 26 / Pin  6
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 27 / Pin  7
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 28 / Pin  8
		IOPortTag & x"03" & PWMTag    & PWMBDirPin,			-- I/O 29 / Pin  9: SPINDLE_DIR
		IOPortTag & x"03" & PWMTag    & PWMAOutPin,			-- I/O 30 / Pin 10: SPINDLE_PWM
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 31 / Pin 11
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 32 / Pin 12
		IOPortTag & x"00" & NullTag    & x"00",				-- I/O 33 / Pin 13

		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin, -- added for 34 pin 5I25
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,


		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin, -- added for IDROM v3
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
					
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,
		emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin,emptypin);

end package PIN_HACKLAB_6I25;
