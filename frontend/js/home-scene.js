import * as THREE from "../vendor/three.module.js";

const stage = document.querySelector("[data-blood-scene]");
const canvas = stage?.querySelector(".blood-canvas");

if (stage && canvas) {
  const reducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  try {
    const renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
      powerPreference: "low-power",
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 30);
    camera.position.set(0, 0, 6.7);

    scene.add(new THREE.HemisphereLight(0xffead8, 0x173b38, 1.6));

    const keyLight = new THREE.DirectionalLight(0xfff1de, 1.8);
    keyLight.position.set(-3.2, 4.2, 4.5);
    scene.add(keyLight);

    const rimLight = new THREE.PointLight(0xf18268, 5, 12, 2);
    rimLight.position.set(2.6, 0.3, 2.8);
    scene.add(rimLight);

    const fillLight = new THREE.PointLight(0x86c1ad, 3.5, 10, 2);
    fillLight.position.set(-2.8, -1.1, 1.8);
    scene.add(fillLight);

    const dropGroup = new THREE.Group();
    scene.add(dropGroup);

    const bezierPoint = (start, controlA, controlB, end, amount) => {
      const inverse = 1 - amount;
      return new THREE.Vector2(
        inverse ** 3 * start.x +
          3 * inverse ** 2 * amount * controlA.x +
          3 * inverse * amount ** 2 * controlB.x +
          amount ** 3 * end.x,
        inverse ** 3 * start.y +
          3 * inverse ** 2 * amount * controlA.y +
          3 * inverse * amount ** 2 * controlB.y +
          amount ** 3 * end.y,
      );
    };

    const base = new THREE.Vector2(0, -1.22);
    const widest = new THREE.Vector2(0.84, -0.12);
    const tip = new THREE.Vector2(0, 1.14);
    const profile = [
      ...Array.from({ length: 49 }, (_, index) =>
        bezierPoint(
          base,
          new THREE.Vector2(0.64, -1.22),
          new THREE.Vector2(0.84, -0.62),
          widest,
          index / 48,
        ),
      ),
      ...Array.from({ length: 48 }, (_, index) =>
        bezierPoint(
          widest,
          new THREE.Vector2(0.84, 0.38),
          new THREE.Vector2(0.035, 1.05),
          tip,
          (index + 1) / 48,
        ),
      ),
    ];

    const dropGeometry = new THREE.LatheGeometry(profile, 128);
    dropGeometry.computeVertexNormals();

    const dropMaterial = new THREE.MeshPhysicalMaterial({
      color: 0xc84442,
      emissive: 0x270709,
      emissiveIntensity: 0.1,
      metalness: 0.01,
      roughness: 0.48,
      clearcoat: 0.16,
      clearcoatRoughness: 0.42,
    });
    const drop = new THREE.Mesh(dropGeometry, dropMaterial);
    drop.scale.setScalar(0.86);
    drop.rotation.z = -0.08;
    dropGroup.add(drop);

    const haloMaterial = new THREE.MeshBasicMaterial({
      color: 0xe9a17f,
      transparent: true,
      opacity: 0.43,
      side: THREE.DoubleSide,
    });
    const halo = new THREE.Mesh(
      new THREE.TorusGeometry(1.48, 0.008, 6, 120),
      haloMaterial,
    );
    halo.rotation.z = -0.2;
    drop.scale.setScalar(0.86);
    halo.position.z = -0.55;
    dropGroup.add(halo);

    const orbit = new THREE.Mesh(
      new THREE.TorusGeometry(1.68, 0.004, 5, 120),
      new THREE.MeshBasicMaterial({
        color: 0x8db7a5,
        transparent: true,
        opacity: 0.32,
      }),
    );
    orbit.rotation.set(0.35, -0.18, 0.28);
    orbit.position.z = -0.9;
    dropGroup.add(orbit);

    const resize = () => {
      const { width, height } = stage.getBoundingClientRect();
      if (!width || !height) return;
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.render(scene, camera);
    };

    new ResizeObserver(resize).observe(stage);
    resize();
    stage.classList.add("webgl-ready");

    if (!reducedMotion) {
      const pointer = { x: 0, y: 0 };
      const startTime = performance.now();
      let frameId;

      stage.addEventListener("pointermove", (event) => {
        const bounds = stage.getBoundingClientRect();
        pointer.x = ((event.clientX - bounds.left) / bounds.width - 0.5) * 2;
        pointer.y = ((event.clientY - bounds.top) / bounds.height - 0.5) * 2;
      });
      stage.addEventListener("pointerleave", () => {
        pointer.x = 0;
        pointer.y = 0;
      });

      const animate = () => {
        frameId = window.requestAnimationFrame(animate);
        const time = (performance.now() - startTime) * 0.001;
        dropGroup.position.y = Math.sin(time * 0.58) * 0.09;
        dropGroup.rotation.y = Math.sin(time * 0.24) * 0.18 + pointer.x * 0.055;
        dropGroup.rotation.x = pointer.y * 0.035;
        drop.rotation.z = -0.08 + Math.sin(time * 0.38) * 0.025;
        halo.material.opacity = 0.39 + Math.sin(time * 0.62) * 0.035;
        renderer.render(scene, camera);
      };

      animate();
      window.addEventListener(
        "pagehide",
        () => window.cancelAnimationFrame(frameId),
        {
          once: true,
        },
      );
    }
  } catch (error) {
    console.warn("The 3D blood drop is unavailable in this browser.", error);
  }
}
