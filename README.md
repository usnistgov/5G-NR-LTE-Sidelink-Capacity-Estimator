# Introduction
This tool computes the expected link capacity in data rate (Mbit/s) for Sidelink considering 5G New Radio (NR) and Long Term Evolution (LTE) communication standards, as defined by the The 3rd Generation Partnership Project (3GPP). Users can input the respective configuration parameter and evaluate the resulting capacity.

The tool provides side-by-side chart plotting between NR and LTE Sidelink capacities for easy comparison. Data and generated charts can be exported to be used outside the tool.

## New Radio (NR) Sidelink Capacity
![Application Screenshot NR](preview-screenshot-NR.png)

The NR Sidelink capacity calculates the maximum achievable data rate in (Mb/s) in Unicast transmission mode at the public safety band (n14), with feedback-based or blind-based Hybrid automatic repeat request (HARQ) transmission scheme, following the equation:

![Application Screenshot LTE](capacity_eq.png)

where *v<sub>layers</sub>* is the spatial multiplexing number of layers, *Q<sub>m</sub>* is the modulation order, *R<sub>max</sub>* is the coding rate, *N<sub>PRB</sub><sup>BW,&mu;</sup>* is the number of Physical Resource Blocks (PRBs) for a specific bandwidth *BW*, *T<sub>S</sub><sup>&mu;</sup>* is the symbol duration time in seconds for numerology *&mu;*, and *OH* is the overhead ratio.

At n14, the supported configuration is listed as follows:

- *&mu;*: 0, 1;
- *BW*: 10 MHz;

Because of the constraints on *BW*, *N<sub>PRB</sub><sup>BW,&mu;</sup>* can be 52 for *&mu;* = 0 and 24 for *&mu;* = 1. *T<sub>S</sub><sup>&mu;</sup>* is 1 x 10<sup>-3</sup> for *&mu;* = 0 and 0.5 x 10<sup>-3</sup> for *&mu;* = 1.

In addition, to achieve the maximum NR capacity at n14, depending on the user equipment (UE) capability, max *Q<sub>m</sub>* can be 6 (64QAM) or 8 (256QAM), v<sub>layers</sub> can be 1 or 2, and *R<sub>max</sub>* is 948/1024, which is the maximum achievable coding rate.

*OH* is the resource elements (REs) occupied by the overhead components over the total number of available REs for transmission. The overhead components can contain

- Physical Sidelink Control Channel (PSCCH),
- Second-stage Control Information (SCI2) in Physical Sidelink Shared Channel (PSSCH),
- Physical Sidelink Feedback Channel (PSFCH), if feedback-based HARQ is enabled
- Sidelink Synchronization Signal Block, (S-SSB),
- Channel State Information Reference Signal (CSI-RS),
- Demodulation Reference Signal (DM-RS),
- Phase-Tracking Reference Signal (PT-RS),
- Automatic Gain Control (AGC),
- Guard, and
- Redundant data, if blind-based HARQ is enabled.

When feedback-based HARQ is enabled, the PSFCH period can be 1, 2, or 4, in unit of slot, and to achieve the maximum data rate, we assume no retransmission is necessary. When blind-based HARQ is used, the number of transmissions for one transport block (TB) can be from 1 to 32.

The NR Sidelink capacity supports all the configurations as stated above, and based on it, the following items can be calculated:

- Data Rate,
- Average REs per slot for each overhead component, as well as its percent total overhead and percent total resources. 

For computation of multiple configurations, the above items can be displayed by clicking on the corresponding configuration. Each selected configuration can be deleted by depressing the "Delete Selected" button, and all the configurations can be reset to default using the "Reset" button. 

It is also important to note that as subchannel is not critical in our NR sidelink capacity investigation, this software assumes that one subchannel is used, and all of the *N<sub>PRB</sub><sup>BW,&mu;</sup>* are allocated to this single subchannel. Besides, we assume minimum number of S-SSBs is configured, which is one in each 160 ms, and within a sidelink configuration period of 10240 ms, all the rest slots are used as sidelink slots.

## Long Term Evolution (LTE) Sidelink Capacity
![Application Screenshot LTE](preview-screenshot-LTE.png)

The LTE Sidelink capacity is dictated by:
- The duration of the Sidelink period (supported values are defined in 3GPP TS36.331).
- The duration of the physical Sidelink channels within the period, i.e., Physical Sidelink Control Channel (PSCCH) and Physical Sidelink Shared Channel (PSSCH). The PSCCH time length can be set from 2 Subframes to a maximum of 40 Subframes (as defined in 3GPP TS36.213). In LTE 1 Subframe is equal to 1 millisecond. The PSSCH time length is set to occupy the remaining period duration after the preceding PSCCH. Since the objective of this tools is to determine the maximum capacity in data rate, time offset and subframe masking is not considered.
- The selected Modulation and Coding Scheme (MCS) and number or Resource Blocks for data transmission.

## Chart Plotting
![Application Screenshot LTE](preview-screenshot-charts.png)

# Installation Instructions

## Requirements

* Python 3.6+

## Create a virtual environment

```shell
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```shell
pip install -r requirements.txt
```

## Run

```shell
python main.py
```

# Development
Follow the [Installation](#installation) instructions above

## Compiling UI Files

### The Quick Way
There's a convenience script to run the following commands,
be sure virtual environment is activated.
```shell
./compile_ui.sh
```

### Manual

If the UI is updated, then the UI files need to be recompiled, run the
following in the virtual environment

```shell
pyside2-uic main-window.ui > ui_mainwindow.py
pyside2-uic csv_dialog.ui > ui_csvdialog.py
```
