<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<div align="center">

<!-- [![Contributors][contributors-shield]][contributors-url] -->
<!-- [![Forks][forks-shield]][forks-url] -->
<!-- [![Stargazers][stars-shield]][stars-url] -->

[![Issues][issues-shield]][issues-url] [![AFL License][license-shield]][license-url]

<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<!-- PROJECT LOGO -->

  <!-- <a href="https://github.com/rsonger/pycg-framework">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

# PyCG Framework

A framework for rendering 3D computer graphics with Python.
<!-- <br />
<a href="https://github.com/rsonger/pycg-framework"><strong>Explore the docs »</strong></a> -->
<!-- <a href="https://github.com/rsonger/pycg-framework">View Demo</a>
· -->
[Report Bug][issues-url] · [Request Feature][issues-url]
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <!-- <li><a href="#usage">Usage</a></li> -->
    <!-- <li><a href="#roadmap">Roadmap</a></li> -->
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This 3D CG graphics framework was created using Python for the purposes of teaching Computer Graphics and Software Engineering through the object-oriented design and application of a CG rendering library. The framework is largely adapted from the same one developed by Lee Stemkoski and Michael Pascale (see [Acknowledgments](#acknowledgments)) with modifications to improve its cross-compatibility, follow object-oriented design principles, and make the source code more pythonic.

For more information on the course in which this framework is being used, see the [Software Engineering Lab](https://robsonger.dev/software-engineering-lab/) website and its posts for individual lessons.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![Pygame][Pygame]][Pygame-url]
* [![PyOpenGL][PyOpenGL]][PyOpenGL-url]

<div align="right">
(<a href="#readme-top">back to top</a>)
</div>


<!-- GETTING STARTED -->
## Getting Started

The following instructions describe how to create a local copy of the framework and configure it to run in a virtual environment.

### Prerequisites

This project requires **Python 3.7+** and it is recommended to use a virtual environment for installing all the dependencies. Either **venv** or **Pipenv** work fine.
* [Python][Python-url]
* [venv](https://docs.python.org/3/library/venv.html)
* [Pipenv](https://pipenv.pypa.io/)

### Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/rsonger/pycg-framework.git
   ```
2. Create a virtual environment.
  **venv**
   ```sh
   python -m venv .venv
   ```
   **Pipenv**
   ```sh
   pipenv install
   ```
3. Activate the virtual environment.
   **venv**
   ```sh
   # Windows
   source .venv/Scripts/activate
   # MacOS
   source .venv/bin/activate
   ```
   **Pipenv**
   ```sh
   pipenv shell
   ```
4. In **venv**, the packages need to be installed after activating the environment.
   ```sh
   pip install -r requirements.txt
   ```
5. On **MacOS**, a discrepency in the OpenGL package may result in an `ImportError`. You can test this by running the following command in the terminal:
   ```sh
   python -c "import OpenGL.GL"
   ```
   If you see the error, look at the Traceback and find the location of the `site-packages\OpenGL\platform` directory inside your Python library. Open the `ctypesloader.py` file from that directory and find the line that has:
   ```python
   fullName = util.find_library( name )
   ```
   Then change the line to:
   ```python
   fullName = f"/System/Library/Frameworks/{name}.framework/{name}"
   ```

<div align="right">
(<a href="#readme-top">back to top</a>)
</div>



<!-- USAGE EXAMPLES -->
<!-- ## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<div align="right">
(<a href="#readme-top">back to top</a>)
</div> -->



<!-- ROADMAP -->
<!-- ## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/rsonger/pycg-framework/issues) for a full list of proposed features (and known issues).

<div align="right">
(<a href="#readme-top">back to top</a>)
</div> -->



<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<div align="right">
(<a href="#readme-top">back to top</a>)
</div> -->



<!-- LICENSE -->
## License

Distributed under the [Academic Free License](https://opensource.org/licenses/AFL-3.0). See `LICENSE.txt` for more information.

<div align="right">
(<a href="#readme-top">back to top</a>)
</div>



<!-- CONTACT -->
## Contact

Rob Songer
[![Website][website-shield]][website-url]

Project Link: [https://github.com/rsonger/pycg-framework](https://github.com/rsonger/pycg-framework)

<div align="right">
(<a href="#readme-top">back to top</a>)
</div>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Lee Stemkoski and Michael Pascale (2021). *Developing Graphics Frameworks with Python and OpenGL*. CRC Press, [in print](https://www.routledge.com/Developing-Graphics-Frameworks-with-Python-and-OpenGL/Stemkoski-Pascale/p/book/9780367721800) and [online](https://www.taylorfrancis.com/books/oa-mono/10.1201/9781003181378/developing-graphics-frameworks-python-opengl-lee-stemkoski-michael-pascale). DOI: [10.1201/9781003181378](https://doi.org/10.1201/9781003181378)

<div align="right">
(<a href="#readme-top">back to top</a>)
</div>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/rsonger/pycg-framework.svg?style=flat-square -->
<!-- [contributors-url]: https://github.com/rsonger/pycg-framework/graphs/contributors -->
<!-- [forks-shield]: https://img.shields.io/github/forks/rsonger/pycg-framework.svg?style=flat-square -->
<!-- [forks-url]: https://github.com/rsonger/pycg-framework/network/members -->
<!-- [stars-shield]: https://img.shields.io/github/stars/rsonger/pycg-framework.svg?style=flat-square -->
<!-- [stars-url]: https://github.com/rsonger/pycg-framework/stargazers -->
[issues-shield]: https://img.shields.io/github/issues/rsonger/pycg-framework.svg?style=flat-square
[issues-url]: https://github.com/rsonger/pycg-framework/issues
[license-shield]: https://img.shields.io/github/license/rsonger/pycg-framework.svg?style=flat-square
[license-url]: https://github.com/rsonger/pycg-framework/blob/master/LICENSE.txt
[website-shield]: https://img.shields.io/website?style=flat-square&url=https%3A%2F%2Frobsonger.dev%2F
[website-url]: https://robsonger.dev/
<!-- [product-screenshot]: screenshots/axes_and_grid.png -->
[Python]: https://img.shields.io/github/pipenv/locked/python-version/rsonger/pycg-framework?style=flat-square
[Python-url]: https://www.python.org/
[Pygame]: https://img.shields.io/badge/Pygame-2.1.1-brightgreen?style=flat-square
[Pygame-url]: https://pygame.org/
[PyOpenGL]: https://img.shields.io/badge/PyOpenGL-3.1.5-lightgrey?style=flat-square
[PyOpenGL-url]: http://pyopengl.sourceforge.net/