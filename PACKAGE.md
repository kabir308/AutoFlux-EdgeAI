# Package Information - AutoFlux-EdgeAI

## Package Metadata

**Name**: autoflux-edgeai  
**Version**: 1.0.0  
**Author**: kabir308  
**License**: MIT  
**Python Requires**: >=3.8  

## PyPI Installation

```bash
pip install autoflux-edgeai
```

## Development Installation

```bash
git clone https://github.com/kabir308/AutoFlux-EdgeAI.git
cd AutoFlux-EdgeAI
pip install -e .
```

## Package Structure

```
autoflux-edgeai/
├── src/
│   ├── autonomous_vehicle/    # Vehicle diagnostics and control
│   ├── neuroflux/             # Edge AI inference
│   └── integration/           # System integration
├── tests/                     # Test suite
├── config/                    # Configuration files
├── docs/                      # Documentation
└── examples/                  # Usage examples
```

## Dependencies

### Core Dependencies
- numpy>=1.21.0
- pandas>=1.3.0
- opencv-python>=4.5.0
- torch>=1.10.0
- onnxruntime>=1.10.0
- python-can>=4.0.0
- fastapi>=0.70.0
- uvicorn>=0.15.0
- pyyaml>=6.0

### Development Dependencies
- pytest>=7.0.0
- pytest-cov>=3.0.0
- black>=22.0.0
- flake8>=4.0.0
- mypy>=0.950

See `requirements.txt` for complete list.

## Classifier Tags

- Development Status :: 4 - Beta
- Intended Audience :: Developers
- Intended Audience :: Science/Research
- License :: OSI Approved :: MIT License
- Operating System :: OS Independent
- Programming Language :: Python :: 3
- Programming Language :: Python :: 3.8
- Programming Language :: Python :: 3.9
- Programming Language :: Python :: 3.10
- Topic :: Scientific/Engineering :: Artificial Intelligence
- Topic :: Software Development :: Embedded Systems

## Compatibility

### Operating Systems
- ✅ Linux (Ubuntu 18.04+, Debian 10+)
- ✅ macOS (10.15+)
- ✅ Windows 10/11

### Python Versions
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ⚠️ Python 3.11 (in testing)

### Hardware Architectures
- ✅ x86_64 (Intel/AMD)
- ✅ ARM64 (Raspberry Pi 4, NVIDIA Jetson)
- ⚠️ ARM32 (limited support)

## Package Size

| Component | Size |
|-----------|------|
| Source code | ~500 KB |
| Documentation | ~50 KB |
| Tests | ~100 KB |
| Examples | ~20 KB |
| **Total (without deps)** | **~670 KB** |

With dependencies: ~1 GB (includes PyTorch, OpenCV)

## Entry Points

```python
# Main system
from src.integration import AutoFluxSystem

# Autonomous vehicle
from src.autonomous_vehicle import DiagnosticSystem, VehicleController, SensorManager

# NeuroFlux AI
from src.neuroflux import InferenceEngine, ModelManager, DataPreprocessor
```

## Configuration

Default configuration file: `config/config.yaml`

Environment variable: `AUTOFLUX_CONFIG_PATH`

```bash
export AUTOFLUX_CONFIG_PATH=/path/to/config.yaml
python your_script.py
```

## Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific module
pytest tests/autonomous_vehicle/
```

## Documentation

- **Online**: https://kabir308.github.io/AutoFlux-EdgeAI/
- **Local**: See `docs/` directory
- **API Reference**: https://kabir308.github.io/AutoFlux-EdgeAI/api.html

## Support Channels

- **Issues**: https://github.com/kabir308/AutoFlux-EdgeAI/issues
- **Discussions**: https://github.com/kabir308/AutoFlux-EdgeAI/discussions
- **Pull Requests**: https://github.com/kabir308/AutoFlux-EdgeAI/pulls

## Changelog

### Version 1.0.0 (2025-11-02)

**Initial Release**

- ✅ Autonomous vehicle module with diagnostics, control, and sensors
- ✅ NeuroFlux edge AI module with inference engine and model management
- ✅ Integration module with orchestrator and REST API
- ✅ Complete test suite (51 tests, 100% pass)
- ✅ Comprehensive documentation
- ✅ GitHub Pages site
- ✅ 0 security vulnerabilities (CodeQL)

## Roadmap

### v1.1.0 (Planned)
- [ ] WebSocket support for real-time monitoring
- [ ] Dashboard web interface
- [ ] Additional model types support
- [ ] Enhanced CAN bus integration

### v1.2.0 (Planned)
- [ ] V2V communication
- [ ] HD Maps integration
- [ ] Advanced path planning
- [ ] Online learning capabilities

## Contributing

See [DEVELOPMENT.md](docs/development.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Homepage**: https://github.com/kabir308/AutoFlux-EdgeAI  
**Documentation**: https://kabir308.github.io/AutoFlux-EdgeAI/  
**Author**: kabir308  
**Email**: Available on GitHub profile
