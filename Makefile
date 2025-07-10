# Makefile for wfx-led-panel simulator
# Uses sdl2-config to get SDL2 compilation flags

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -g -DSIMULATOR -DARDUINO=100

# SDL2 flags from sdl2-config
SDL2_CFLAGS := $(shell sdl2-config --cflags)
SDL2_LIBS := $(shell sdl2-config --libs) -lutil

# Include directories
INCLUDES = -Iinclude/sim -Ilib/Adafruit_GFX_Library

# Directories
SRCDIR = src
LIBDIR = lib/Adafruit_GFX_Library
BUILDDIR = build

# Source files
SOURCES = $(wildcard $(SRCDIR)/*.cpp) $(LIBDIR)/Adafruit_GFX.cpp
OBJECTS = $(SOURCES:%.cpp=$(BUILDDIR)/%.o)

# Target executable
TARGET = $(BUILDDIR)/wfx-led-panel-sim

# Default target
all: $(TARGET)

# Build the executable
$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET) $(SDL2_LIBS)

# Create build directories
$(BUILDDIR)/$(SRCDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(BUILDDIR)/$(SRCDIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SDL2_CFLAGS) -c $< -o $@

$(BUILDDIR)/$(LIBDIR)/%.o: $(LIBDIR)/%.cpp
	@mkdir -p $(BUILDDIR)/$(LIBDIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SDL2_CFLAGS) -c $< -o $@

# Legacy rule (kept for compatibility)
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SDL2_CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -rf $(BUILDDIR)

# Install dependencies (macOS)
install-deps:
	brew install sdl2

# Run the simulator
run: $(TARGET)
	./$(TARGET)

# Debug build
debug: CXXFLAGS += -DDEBUG -O0
debug: $(TARGET)

# Release build
release: CXXFLAGS += -O2 -DNDEBUG
release: $(TARGET)

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Build the simulator (default)"
	@echo "  clean      - Remove build artifacts"
	@echo "  install-deps - Install SDL2 dependency (macOS)"
	@echo "  run        - Build and run the simulator"
	@echo "  debug      - Build with debug flags"
	@echo "  release    - Build with optimization flags"
	@echo "  help       - Show this help message"

.PHONY: all clean install-deps run debug release help 