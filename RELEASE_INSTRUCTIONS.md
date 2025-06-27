# PyPI Release Instructions

## Package Release for fast_images_loader v0.2.0

The package has been successfully built and is ready for release! Here are the steps to complete the PyPI upload:

### Files Ready for Upload:
- `dist/fast_images_loader-0.2.0-py3-none-any.whl` (wheel distribution)
- `dist/fast_images_loader-0.2.0.tar.gz` (source distribution)

### What's New in v0.2.0:
✅ Video loading support with async processing
✅ Frame extraction from videos at configurable rates
✅ Enhanced CLI with auto media type detection
✅ New FastVideosLoader class for specialized video handling
✅ Support for multiple video formats (mp4, avi, mov, mkv, etc.)
✅ Comprehensive test coverage

### Release Steps:

1. **Create PyPI API Token** (if not already done):
   - Go to https://pypi.org/manage/account/
   - Create a new API token with project scope for "fast_images_loader"
   - Save the token securely

2. **Upload to TestPyPI** (optional, for testing):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
   - Enter your TestPyPI API token when prompted
   - Test the installation: `pip install --index-url https://test.pypi.org/simple/ fast_images_loader==0.2.0`

3. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```
   - Enter your PyPI API token when prompted

4. **Verify the Release**:
   - Check https://pypi.org/project/fast_images_loader/
   - Test installation: `pip install fast_images_loader==0.2.0`
   - Test the new video functionality

### Post-Release:
- Update GitHub repository with the new tag: `git tag v0.2.0 && git push origin v0.2.0`
- Create a GitHub release with the CHANGELOG
- Update documentation if needed

### Package Quality Checks:
✅ All tests passing (4/4)
✅ Package structure validated
✅ Dependencies properly declared
✅ README updated with video examples
✅ CHANGELOG created
✅ Version bumped to 0.2.0

The package is ready for release! 🚀
